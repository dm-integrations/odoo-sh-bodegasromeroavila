# -*- coding: utf-8 -*-
from odoo import models, api, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def _search_fetch(self, search_detail, search, limit, order):
        # Aseguramos que la búsqueda de plantillas sea limpia
        results, count = super(ProductTemplate, self)._search_fetch(search_detail, search, limit, order)
        return results, count


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def _search_fetch(self, search_detail, search, limit, order):
        # Si la consulta de búsqueda en la web se realiza directamente sobre variantes (product.product),
        # agrupamos por plantilla de producto para que en la web sólo figure una variante única por cada plantilla.
        results, count = super(ProductProduct, self)._search_fetch(search_detail, search, limit, order)
        
        if search_detail.get('model') == 'product.product' and results:
            seen_templates = set()
            filtered_results = self.env['product.product']
            for prod in results:
                if prod.product_tmpl_id.id not in seen_templates:
                    seen_templates.add(prod.product_tmpl_id.id)
                    filtered_results |= prod
            results = filtered_results
            count = len(results)
            
        return results, count
