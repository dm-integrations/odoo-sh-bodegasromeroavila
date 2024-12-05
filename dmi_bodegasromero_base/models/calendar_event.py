from odoo import models, api, fields, _


class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    def _prepare_notification_vals(self, vals):
        body = ""
        ir_models_field_obj = self.env['ir.model.fields']
        for item in list(vals.keys()):
            field_id = ir_models_field_obj.sudo().with_context(lang='es_ES').search([
                ('name', '=', item),
            ], limit=1)

            body += "Se ha modificado el evento %s: %s\n" % (field_id.name or item, vals[item])
        return body

    #Utilizaremos este metodo para notificar a todos cuando ocurra una modificacion
    def action_sendmail(self, vals):
        email = self.env.user.email
        attendee_ids = self.attendee_ids.filtered(lambda k:k.partner_id.id != self.env.user.partner_id.id)
        if email:
            for meeting in self:
                for attendee in attendee_ids:
                    body = meeting._prepare_notification_vals(vals)
                    subject = meeting.name

                    self.sudo().message_notify(
                        email_from=attendee.event_id.user_id.email_formatted or self.env.user.email_formatted,
                        author_id=attendee.event_id.user_id.partner_id.id or self.env.user.partner_id.id,
                        body=body,
                        subject=subject,
                        partner_ids=attendee.partner_id.ids,
                        email_layout_xmlid='mail.mail_notification_light',
                        attachment_ids=False,
                        force_send=True,
                    )
        return True

    def write(self, vals):
        res = super().write(vals)
        self.action_sendmail(vals)
        return res
