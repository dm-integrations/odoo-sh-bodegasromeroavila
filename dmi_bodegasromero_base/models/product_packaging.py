from odoo import models, api, fields, _


class ProductPackaging(models.Model):

    _inherit = "product.packaging"

    name = fields.Char(
        string="Nombre",
        required=True,
        translate=True,
    )
