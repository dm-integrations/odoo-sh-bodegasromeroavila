from odoo import models, api, fields, _


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
            self.env["mail.activity"].create(
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
            ('date_deadline', '!=', False),
            ('date_deadline', '<=', fields.Date.today()),
        ]):
            task.set_task_activity()

    def _prepare_event_vals(self, vals):
        follower_partner_ids = self.user_ids.mapped('partner_id') \
            if self.user_ids else []
        values = {
            "name": vals.get("name") if vals.get("name") else self.name,
            "start": vals.get("planned_date_begin") if vals.get("planned_date_begin") else self.planned_date_begin,
            "stop": vals.get("date_deadline") if vals.get("date_deadline") else self.date_deadline,
            "description": vals.get("description") if vals.get("description") else self.description,
            "partner_ids": [(6, 0, follower_partner_ids.ids)]
            if follower_partner_ids else [(6, 0, self.env.user.partner_id.ids)],
            "active": True,
            "task_id": self.id
        }

        return values

    def _upsert_calendar_event(self, vals):
        if self.dmi_calendar_event_id:
            values = self._prepare_event_vals(vals)
            self.dmi_calendar_event_id.update(values)
        else:
            values = self._prepare_event_vals(vals)
            calendar_event_id = self.env["calendar.event"].create(values)
            self.with_context(no_update=True).update({"dmi_calendar_event_id": calendar_event_id.id})

    @api.model_create_multi
    def create(self, vals_list):
        tasks = super().create(vals_list)
        for vals in vals_list:
            if 'planned_date_begin' in vals and vals.get('planned_date_begin'):
                self._upsert_calendar_event(vals)
        return tasks

    def write(self, vals):
        res = super().write(vals)
        # Comprobamos si hay fecha de inicio o final en la tarea o si ya tiene un evento de calendario asociado
        # self.planned_date_begin es basicamente por historias anteriores a la personalizacion
        if self.env.context.get("no_update"):
            return res
        if 'planned_date_begin' in vals or 'date_deadline' in vals \
                or self.planned_date_begin or self.dmi_calendar_event_id:
            self._upsert_calendar_event(vals)
        return res
