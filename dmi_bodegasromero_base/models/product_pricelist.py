from odoo import models, api, fields, _


class ProductPricelist(models.Model):

    _inherit = "product.pricelist"

    no_show_in_list = fields.Boolean(
        string="No mostrar tarifa en listado",
        default=False,
    )
