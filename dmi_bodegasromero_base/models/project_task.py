from odoo import models, api, fields, _
from datetime import datetime, timedelta


class ProjectTask(models.Model):
    _inherit = "project.task"

    dmi_calendar_event_id = fields.Many2one(
        "calendar.event",
        string="Evento de Calendario",
        readonly=True,
    )

    def action_open_calendar_event(self):
        self.ensure_one()
        return {
            "name": _("Evento de Calendario"),
            "type": "ir.actions.act_window",
            "res_model": "calendar.event",
            "view_mode": "form",
            "res_id": self.dmi_calendar_event_id.id,
            "target": "current",
        }

    def set_task_activity(self):
        for user in self.user_ids:
            self.env["mail.activity"].sudo().create(
                {
                    "activity_type_id": self.env.ref("mail.mail_activity_data_todo").id,
                    "summary": "Tarea fuera de fecha límit: " + self.name,
                    "res_id": self.id,
                    "res_model_id": self.env.ref("project.model_project_task").id,
                    "date_deadline": fields.Date.today(),
                    "user_id": user.id,
                }
            )

    def create_activity_date_limit(self):
        for task in self.search([
            ('state', 'not in', ("1_done", "1_canceled")),
            ('date_deadline', '!=', False),
            ('date_deadline', '<=', fields.Date.today()),
        ]):
            task.set_task_activity()

    def _prepare_event_vals(self, vals):
        follower_partner_ids = self.user_ids.mapped('partner_id') \
            if self.user_ids else []
        start_date = vals.get("planned_date_begin") if vals.get("planned_date_begin") else self.planned_date_begin
        end_date = vals.get("date_deadline") if vals.get("date_deadline") else self.date_deadline
        # Si no se indicara fecha de inicio por defecto restamos una hora
        if not start_date:
            start_date_dt = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S") + timedelta(hours=-1) \
                if isinstance(end_date, str) else end_date + timedelta(hours=-1)
            start_date = start_date_dt.strftime("%Y-%m-%d %H:%M:%S")

        values = {
            "name": vals.get("name") if vals.get("name") else self.name,
            "start": start_date,
            "stop": vals.get("date_deadline") if vals.get("date_deadline") else self.date_deadline,
            "description": vals.get("description") if vals.get("description") else self.description,
            "partner_ids": [(6, 0, follower_partner_ids.ids)]
            if follower_partner_ids else [(6, 0, self.env.user.partner_id.ids)],
            "active": True,
            "task_id": self.id
        }

        return values

    def _upsert_calendar_event(self, vals):
        self.ensure_one()
        if self.dmi_calendar_event_id:
            values = self._prepare_event_vals(vals)
            self.dmi_calendar_event_id.sudo().update(values)
        else:
            values = self._prepare_event_vals(vals)
            calendar_event_id = self.env["calendar.event"].sudo().create(values)
            self.with_context(no_update=True).update({"dmi_calendar_event_id": calendar_event_id.id})

    @api.model_create_multi
    def create(self, vals_list):
        tasks = super().create(vals_list)
        for task, vals in zip(tasks, vals_list):
            if vals.get('planned_date_begin'):
                task._upsert_calendar_event(vals)
        return tasks

    def write(self, vals):
        res = super().write(vals)
        if self.env.context.get("no_update"):
            return res
        if 'planned_date_begin' in vals or 'date_deadline' in vals:
            for task in self:
                if task.planned_date_begin or task.dmi_calendar_event_id:
                    task._upsert_calendar_event(vals)
        return res
