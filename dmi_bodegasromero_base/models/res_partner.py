from odoo import models, api, fields, _
import json


class ResPartner(models.Model):
    _inherit = "res.partner"

    user_id = fields.Many2one(
        default=lambda self: self.env.user,
        comodel_name="res.users",
        string="Comercial",
        tracking=True,
        required=True,
    )
    tapon = fields.Selection(
        string="Tapón",
        selection=[
            ("corcho", "Corcho"),
            ("rosca", "Rosca"),
        ],
    )
