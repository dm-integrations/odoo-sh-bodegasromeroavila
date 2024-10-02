from odoo import models, api, fields, _


class CrmLead(models.Model):
    _inherit = "crm.lead"

    fuente = fields.Char(
        string="Fuente",
    )
    vat = fields.Char(
        string="CIF",
        related="partner_id.vat",
        readonly=False,
        store=True,
    )
