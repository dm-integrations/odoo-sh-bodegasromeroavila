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
    user_ids = fields.Many2many(
        default=lambda self: self.env.user,
        comodel_name="res.users",
        string="Seguidores",
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
    fuente_id = fields.Many2one(
        string="Fuente",
        comodel_name="crm.lead.fuente",
    )
    partner_vinculado_id = fields.Many2one(
        string="Cliente Vinculado",
        comodel_name="res.partner",
        domain=[("is_company", "=", True)]
    )
