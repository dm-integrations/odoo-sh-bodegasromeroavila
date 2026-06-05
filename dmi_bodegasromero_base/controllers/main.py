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
        _logger.info("ROMERO SHOP DEBUG: Model is %s, count: %s", search_result._name, len(search_result))
        for p in search_result[:15]:
            _logger.info("ROMERO SHOP DEBUG: ID=%s, Name=%s, TempID=%s", p.id, p.name, p.product_tmpl_id.id if p._name == 'product.product' else p.id)

        if search_result._name == 'product.product':
            # Si se está forzando la búsqueda sobre variantes (product.product),
            # filtramos las variantes para conservar únicamente una de cada plantilla. También por nombre limpio.
            templates_seen = set()
            names_seen = set()
            filtered_results = request.env['product.product']
            for prod in search_result:
                tmpl_id = prod.product_tmpl_id.id
                name_key = prod.name.strip().lower() if prod.name else ""
                if tmpl_id not in templates_seen and (not name_key or name_key not in names_seen):
                    templates_seen.add(tmpl_id)
                    if name_key:
                        names_seen.add(name_key)
                    filtered_results |= prod
            search_result = filtered_results
            product_count = len(search_result)

        elif search_result._name == 'product.template':
            # Si el buscador devuelve plantillas de producto pero existiera duplicidad de nombres o IDs
            # debido a variantes cargadas como plantillas separadas o atributos mal configurados,
            # garantizamos que el anuncio mostrado sea totalmente único en la interfaz web de la tienda.
            templates_seen = set()
            names_seen = set()
            filtered_results = request.env['product.template']
            for tmpl in search_result:
                name_key = tmpl.name.strip().lower() if tmpl.name else ""
                if tmpl.id not in templates_seen and (not name_key or name_key not in names_seen):
                    templates_seen.add(tmpl.id)
                    if name_key:
                        names_seen.add(name_key)
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
        seen_names = set()
        filtered_products = []
        is_product_product = (products._name == 'product.product')
        is_modified = False
        
        for prod in products:
            tmpl_id = prod.product_tmpl_id.id if is_product_product else prod.id
            prod_name = prod.name.strip().lower() if prod.name else ""
            
            # Filtro robusto que agrupa tanto por plantilla (ID físico) como por nombre del producto
            if tmpl_id not in seen_templates and (not prod_name or prod_name not in seen_names):
                seen_templates.add(tmpl_id)
                if prod_name:
                    seen_names.add(prod_name)
                filtered_products.append(prod)
            else:
                is_modified = True
                _logger.info("ROMERO SHOP DEDUPLICATE: Ignorando duplicado de producto ID=%s, Name=%s", prod.id, prod.name)
                
        if is_modified:
            # Si detectamos que de verdad quedan duplicados de variante en la renderización, los limpiamos de forma definitiva
            filtered_recordset = request.env[products._name].browse([p.id for p in filtered_products])
            values['products'] = filtered_recordset
            values['bins'] = TableCompute().process(filtered_recordset, values.get('ppg', 20), values.get('ppr', 4))
            
    return res

WebsiteSale._get_additional_extra_shop_values = _get_additional_extra_shop_values_patched
