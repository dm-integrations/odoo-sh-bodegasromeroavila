from odoo import models, api, fields, _


class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    team_id = fields.Many2one(
        'crm.team',
        string='Departamento'
    )

    @api.onchange('team_id')
    def _onchange_team_id(self):
        if self.team_id:
            self.partner_ids = self.team_id.mapped("member_ids.partner_id") if self.team_id.member_ids else False


class Contacts(models.Model):
    _inherit = 'calendar.filters'

    team_id = fields.Many2one('crm.team', 'Departamento', required=True, index=True)
