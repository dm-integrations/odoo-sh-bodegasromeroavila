from odoo import models, api, fields, _
import json


class DmiProductComponent(models.Model):
    _name = 'dmi.product.component'
    _description = 'Product Component'

    name = fields.Char(
        string='Nombre',
        required=True,
        translate=True
    )
    price_unit = fields.Float(
        string="Precio unitario",
        digits="Decimales scrap",
    )
    price_weight = fields.Float(
        string="Precio por peso",
        digits="Decimales scrap",
    )
    exclude_not_packaging = fields.Boolean(
        string="Excluir si no está empaquetado",
        default=False,
    )
