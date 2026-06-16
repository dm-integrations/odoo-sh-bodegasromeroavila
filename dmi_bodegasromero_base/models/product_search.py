# -*- coding: utf-8 -*-
from odoo import models, api

from odoo.addons.dmi_bodegasromero_base.tools import clean_product_name as _clean_product_name
from odoo.addons.dmi_bodegasromero_base.tools import strip_size_suffix


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def website_clean_name(self):
        """Nombre del producto sin el sufijo de talla, para mostrarlo en la tienda web."""
        self.ensure_one()
        return strip_size_suffix(self.display_name) or self.display_name

    @api.depends('name', 'default_code')
    @api.depends_context('website_strip_size')
    def _compute_display_name(self):
        super()._compute_display_name()
        if self.env.context.get('website_strip_size'):
            for tmpl in self:
                if tmpl.display_name:
                    tmpl.display_name = strip_size_suffix(tmpl.display_name) or tmpl.display_name

    @api.model
    def _search_fetch(self, search_detail, search, limit, order):
        # Aseguramos que la búsqueda de plantillas sea limpia
        results, count = super(ProductTemplate, self)._search_fetch(search_detail, search, limit, order)
        
        if results:
            from odoo.http import request
            # Solo aplicamos el filtro si estamos dentro de una petición web (e-commerce)
            if request and getattr(request, 'website', None):
                seen_templates = set()
                seen_names = set()
                filtered_results = self.env['product.template']
                for tmpl in results:
                    name_key = _clean_product_name(tmpl.name)
                    if tmpl.id not in seen_templates and (not name_key or name_key not in seen_names):
                        seen_templates.add(tmpl.id)
                        if name_key:
                            seen_names.add(name_key)
                        filtered_results |= tmpl
                results = filtered_results
                count = len(results)
                
        return results, count


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def website_clean_name(self):
        """Nombre de la variante sin el sufijo de talla, para mostrarlo en la tienda web."""
        self.ensure_one()
        return strip_size_suffix(self.display_name) or self.display_name

    @api.depends('name', 'default_code', 'product_tmpl_id')
    @api.depends_context(
        'display_default_code', 'seller_id', 'company_id', 'partner_id',
        'use_partner_name', 'website_strip_size',
    )
    def _compute_display_name(self):
        super()._compute_display_name()
        if self.env.context.get('website_strip_size'):
            for prod in self:
                if prod.display_name:
                    prod.display_name = strip_size_suffix(prod.display_name) or prod.display_name

    @api.model
    def _search_fetch(self, search_detail, search, limit, order):
        # Si la consulta de búsqueda en la web se realiza directamente sobre variantes (product.product),
        # agrupamos por plantilla de producto para que en la web sólo figure una variante única por cada plantilla.
        results, count = super(ProductProduct, self)._search_fetch(search_detail, search, limit, order)
        
        if results:
            from odoo.http import request
            if request and getattr(request, 'website', None):
                seen_templates = set()
                seen_names = set()
                filtered_results = self.env['product.product']
                for prod in results:
                    tmpl_id = prod.product_tmpl_id.id
                    name_key = _clean_product_name(prod.name)
                    if tmpl_id not in seen_templates and (not name_key or name_key not in seen_names):
                        seen_templates.add(tmpl_id)
                        if name_key:
                            seen_names.add(name_key)
                        filtered_results |= prod
                results = filtered_results
                count = len(results)
            
        return results, count
