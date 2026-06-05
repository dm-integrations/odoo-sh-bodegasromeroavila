# -*- coding: utf-8 -*-
import logging
from odoo.addons.website_sale.controllers.main import WebsiteSale, TableCompute

from odoo.addons.dmi_bodegasromero_base.tools import clean_product_name

_logger = logging.getLogger(__name__)


def _dedupe_recordset(records):
    """
    Devuelve un recordset (mismo modelo que `records`) sin duplicados, agrupando por
    plantilla de producto y por nombre base limpio (sin sufijos de talla).
    Soporta tanto product.product como product.template.
    Devuelve la tupla (recordset, modificado).
    """
    if not records:
        return records, False

    is_product_product = records._name == 'product.product'
    seen_templates = set()
    seen_names = set()
    kept_ids = []
    modified = False

    for rec in records:
        tmpl_id = rec.product_tmpl_id.id if is_product_product else rec.id
        name_key = clean_product_name(rec.name)
        if tmpl_id not in seen_templates and (not name_key or name_key not in seen_names):
            seen_templates.add(tmpl_id)
            if name_key:
                seen_names.add(name_key)
            kept_ids.append(rec.id)
        else:
            modified = True
            _logger.info(
                "ROMERO SHOP DEDUPLICATE: Ignorando duplicado ID=%s, Name=%s, CleanName=%s",
                rec.id, rec.name, name_key,
            )

    if not modified:
        return records, False

    # Mantenemos el orden original respetando los ids conservados
    return records.browse(kept_ids), True


class WebsiteSaleDmi(WebsiteSale):

    def _shop_lookup_products(self, attrib_set, options, post, search, website):
        fuzzy_search_term, product_count, search_result = super()._shop_lookup_products(
            attrib_set, options, post, search, website
        )
        if search_result:
            _logger.info(
                "ROMERO SHOP DEBUG: Model=%s, count=%s, website=%s",
                search_result._name, len(search_result), website.name,
            )
            deduped, modified = _dedupe_recordset(search_result)
            if modified:
                search_result = deduped
                product_count = len(search_result)
        return fuzzy_search_term, product_count, search_result

    def _get_additional_extra_shop_values(self, values, **post):
        res = super()._get_additional_extra_shop_values(values, **post)
        products = values.get('products')
        if products:
            deduped, modified = _dedupe_recordset(products)
            if modified:
                values['products'] = deduped
                bins = TableCompute().process(deduped, values.get('ppg', 20), values.get('ppr', 4))
                values['bins'] = bins
                if isinstance(res, dict):
                    res['products'] = deduped
                    res['bins'] = bins
        return res
