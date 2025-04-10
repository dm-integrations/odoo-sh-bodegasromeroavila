from odoo import models, api, fields, _
import json


class DmiProductTemplateComponents(models.Model):
    _name = 'dmi.product.template.components'
    _description = 'Product Template Component'

    product_template_id = fields.Many2one(
        comodel_name='product.template',
        string='Producto',
        required=True
    )
    product_component_id = fields.Many2one(
        comodel_name='dmi.product.component',
        string='Componente',
        required=True
    )
    weight = fields.Float(
        string="Peso",
        digits="Decimales peso",
    )
    price_unit = fields.Float(
        string="Precio unitario",
        digits="Decimales scrap",
        related='product_component_id.price_unit',
        readonly=True,
        store=True
    )
    price_weight = fields.Float(
        string="Precio por peso",
        digits="Decimales scrap",
        related='product_component_id.price_weight',
        readonly=True,
        store=True
    )
    quote = fields.Float(
        string="Cuota",
        digits="Decimales quote",
        compute='_compute_quote',
        store=True,
    )
    exclude_not_packaging = fields.Boolean(
        string="Excluir si no está empaquetado",
        related='product_component_id.exclude_not_packaging',
    )

    @api.depends('weight', 'price_unit', 'price_weight')
    def _compute_quote(self):
        for record in self:
            record.quote = record.price_unit + (record.price_weight * record.weight)
