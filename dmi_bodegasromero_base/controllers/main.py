# -*- coding: utf-8 -*-
import logging
from odoo.addons.website_sale.controllers.main import WebsiteSale, TableCompute
from odoo.http import request

_logger = logging.getLogger(__name__)

# --- MONKEYPATCHING _shop_lookup_products ---
original_shop_lookup_products = WebsiteSale._shop_lookup_products

def _shop_lookup_products_patched(self, attrib_set, options, post, search, website):
    fuzzy_search_term, product_count, search_result = original_shop_lookup_products(
        self, attrib_set, options, post, search, website
    )
    if search_result:
        if search_result._name == 'product.product':
            # Si algún módulo de terceros está forzando la búsqueda sobre variantes (product.product),
            # filtramos las variantes para conservar únicamente una variante por plantilla de producto,
            # agrupando e impidiendo que salgan múltiples anuncios por cada talla.
            templates_seen = set()
            filtered_results = request.env['product.product']
            for prod in search_result:
                if prod.product_tmpl_id.id not in templates_seen:
                    templates_seen.add(prod.product_tmpl_id.id)
                    filtered_results |= prod
            search_result = filtered_results
            product_count = len(search_result)

        elif search_result._name == 'product.template':
            # Si el buscador devuelve plantillas de producto pero existiera duplicidad (por ejemplo,
            # si se han generado múltiples plantillas de producto separadas pero con mismo nombre/clúster),
            # garantizamos que el anuncio mostrado sea único en la web.
            templates_seen = set()
            filtered_results = request.env['product.template']
            for tmpl in search_result:
                if tmpl.id not in templates_seen:
                    templates_seen.add(tmpl.id)
                    filtered_results |= tmpl
            search_result = filtered_results
            product_count = len(search_result)

    return fuzzy_search_term, product_count, search_result

WebsiteSale._shop_lookup_products = _shop_lookup_products_patched


# --- MONKEYPATCHING _get_additional_extra_shop_values ---
original_get_additional_extra_shop_values = WebsiteSale._get_additional_extra_shop_values

def _get_additional_extra_shop_values_patched(self, values, **post):
    res = original_get_additional_extra_shop_values(self, values, **post)
    products = values.get('products')
    if products:
        seen_templates = set()
        filtered_products = []
        is_product_product = (products._name == 'product.product')
        is_modified = False
        
        for prod in products:
            tmpl_id = prod.product_tmpl_id.id if is_product_product else prod.id
            if tmpl_id not in seen_templates:
                seen_templates.add(tmpl_id)
                filtered_products.append(prod)
            else:
                is_modified = True
                
        if is_modified:
            # Si detectamos que de verdad quedan duplicados de variante en la renderización, los limpiamos de forma definitiva
            filtered_recordset = request.env[products._name].browse([p.id for p in filtered_products])
            values['products'] = filtered_recordset
            values['bins'] = TableCompute().process(filtered_recordset, values.get('ppg', 20), values.get('ppr', 4))
            
    return res

WebsiteSale._get_additional_extra_shop_values = _get_additional_extra_shop_values_patched
