from odoo import models, api, fields, _


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_image = fields.Image(
        string='Imagen',
        related='product_id.image_128',
    )
