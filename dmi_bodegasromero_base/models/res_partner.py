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
        required=False,
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

    def create_activity(self):
        self.ensure_one()
        self.env["mail.activity"].create(
            {
                "activity_type_id": self.env.ref("mail.mail_activity_data_todo").id,
                "summary": "Revisar nuevo contacto: " + self.name,
                "res_id": self.id,
                "res_model_id": self.env.ref("base.model_res_partner").id,
                "date_deadline": fields.Date.today(),
                "user_id": 2,
            }
        )

    @api.model_create_multi
    def create(self, vals_list):
        res = super(ResPartner, self).create(vals_list)
        for vals in vals_list:
            if vals.get("is_company"):
                for record in res:
                    record.create_activity()
        return res
