from odoo import models, api, fields, _
from datetime import timedelta


class ProjectTask(models.Model):
    _inherit = "project.task"

    calendar_event_id = fields.Many2one(
        string="Evento",
        comodel_name="calendar.event"
    )
    attendee_ids = fields.Many2many(
        string="Asistentes",
        comodel_name="res.partner",
        compute="_compute_attendee_ids",
        store=True,
    )

    @api.depends('user_ids')
    def _compute_attendee_ids(self):
        for record in self:
            record.attendee_ids = record.user_ids.mapped('partner_id')

    def action_view_event(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'calendar.event',
            'view_mode': 'form',
            'res_id': self.calendar_event_id.id,
            'target': 'current',
        }

    def upsert_calendar_event(self):
        for task in self:
            date_start = task.planned_date_start if task.planned_date_start else task.date_deadline
            date_end = task.date_deadline + timedelta(hours=1) \
                if not task.planned_date_start else task.date_deadline
            if not task.calendar_event_id:
                task.calendar_event_id = self.env['calendar.event'].create({
                    'name': task.name,
                    'start': date_start,
                    'stop': date_end,
                    'allday': False,
                    'project_id': task.project_id.id,
                    'task_id': task.id,
                    'attendee_ids': [(6, 0, task.attendee_ids.ids)],
                })
                self.with_context(skip_upsert_calendar_event=True).write({
                    'calendar_event_id': task.calendar_event_id.id
                })
            else:
                task.calendar_event_id.write({
                    'name': task.name,
                    'start': date_start,
                    'stop': date_end,
                    'allday': False,
                    'project_id': task.project_id.id,
                    'task_id': task.id,
                    'attendee_ids': [(6, 0, task.attendee_ids.ids)],
                })

    def write(self, vals):
        res = super().write(vals)
        if self.env.context.get('skip_upsert_calendar_event'):
            return
        if 'attendee_ids' in vals or 'planned_date_begin' in vals or 'planned_date_end' in vals:
            self.upsert_calendar_event()
        return res

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        for record in res:
            if record.attendee_ids or record.planned_date_begin or record.planned_date_end:
                record.upsert_calendar_event()
        return res

    def unlink(self):
        for record in self:
            if record.calendar_event_id:
                record.calendar_event_id.unlink()
        return super().unlink()
