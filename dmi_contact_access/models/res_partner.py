from odoo import models, api, fields, _
import json


class ResPartner(models.Model):
    _inherit = "res.partner"

    user_id = fields.Many2one(
        default=lambda self: self.env.user,
        required=True,
    )
