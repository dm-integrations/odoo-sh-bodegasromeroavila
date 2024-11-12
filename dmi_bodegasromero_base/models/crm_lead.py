from odoo import models, api, fields, _


class CrmLead(models.Model):
    _inherit = "crm.lead"

    fuente = fields.Char(
        string="Fuentes",
    )
    fuente_id = fields.Many2one(
        string="Fuente",
        comodel_name="crm.lead.fuente",
    )
    vat = fields.Char(
        string="CIF",
        related="partner_id.vat",
        readonly=False,
        store=True,
    )
