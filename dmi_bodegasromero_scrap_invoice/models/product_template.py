from odoo import models, api, fields, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_template_component_ids = fields.One2many(
        comodel_name='dmi.product.template.components',
        inverse_name='product_template_id',
        string='Componentes',
    )
    total_quotes = fields.Float(
        string='Total Cuotas',
        compute='_compute_total_quotes',
        digits="Decimales scrap",
        store=True,
    )

    @api.depends('product_template_component_ids', 'product_template_component_ids.quote')
    def _compute_total_quotes(self):
        for record in self:
            record.total_quotes = sum(record.product_template_component_ids.mapped('quote'))
