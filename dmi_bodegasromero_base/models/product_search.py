# -*- coding: utf-8 -*-
import re
from odoo import models, api, fields


def _clean_product_name(name):
    if not name:
        return ""
    name = name.strip().lower()
    
    # Soportamos números de 1 o 2 dígitos para tallas de vestir (38, 40, etc.) sin de-duplicar años como "2024"
    size_terms = r'xs|s|m|l|xl|xxl|xxxl|pequeño|pequeña|mediano|mediana|grande|grandes|talla\s*\d+|talla\s*[a-zA-Z]+|\d{1,2}'
    
    # 1. Paréntesis con talla o número: " (s)", " (m)", " (l)", " (xl)", " (xxl)", " (xs)", " (42)", " (talla s)"
    name = re.sub(rf'\s*\((talla\s+)?({size_terms})\)\s*$', '', name, flags=re.IGNORECASE)
    
    # 2. Guión, barra o coma con talla o número: " - s", " - m", " - l", " - xl", " / s", " , s"
    name = re.sub(rf'\s*[\-/,]\s*(talla\s+)?({size_terms})\s*$', '', name, flags=re.IGNORECASE)
    
    # 3. Talla de texto explícita o palabra de talla: "talla s", "talla m", "talla 42"
    name = re.sub(rf'\s+talla\s*({size_terms})\s*$', '', name, flags=re.IGNORECASE)
    
    # 4. Talla suelta al final precedida por un espacio (letras individuales o palabras de tallas comunes)
    name = re.sub(rf'\s+(xs|s|m|l|xl|xxl|xxxl|pequeño|pequeña|mediano|mediana|grande|grandes)\s*$', '', name, flags=re.IGNORECASE)
    
    return name.strip()


class ProductTemplate(models.Model):
    _inherit = 'product.template'

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
