from odoo import models, api, fields, _


class LoyaltyProgram(models.Model):
    _inherit = "loyalty.program"

    partner_ids = fields.Many2many(
        string="Clientes",
        comodel_name="res.partner",
    )
