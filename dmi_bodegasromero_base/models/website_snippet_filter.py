# -*- coding: utf-8 -*-
import logging
from odoo import models, api
from .product_search import _clean_product_name

_logger = logging.getLogger(__name__)


class WebsiteSnippetFilter(models.Model):
    _inherit = 'website.snippet.filter'

    def _filter_records_to_values(self, records, is_sample=False):
        """
        Deduplicamos las plantillas/variantes de producto que tienen el mismo nombre base
        (ignorando los sufijos de talla S/M/L, etc.). Esto evita que en los snippets de
        e-commerce dinámicos aparezcan varias entradas de la misma camiseta por cada talla.
        Solo aplicamos en modelos product.product y product.template.
        """
        if records and not is_sample and records._name in ('product.product', 'product.template'):
            # Limpiamos el sufijo de talla del nombre mostrado en los snippets dinámicos
            # (las plantillas usan record.display_name). Lo hacemos vía contexto para no
            # afectar al carrito/checkout ni al backend.
            records = records.with_context(website_strip_size=True)
            is_product_product = records._name == 'product.product'
            seen_templates = set()
            seen_names = set()
            filtered = records.browse([])
            for rec in records:
                tmpl_id = rec.product_tmpl_id.id if is_product_product else rec.id
                name_key = _clean_product_name(rec.name)
                if tmpl_id not in seen_templates and (not name_key or name_key not in seen_names):
                    seen_templates.add(tmpl_id)
                    if name_key:
                        seen_names.add(name_key)
                    filtered |= rec
                else:
                    _logger.info(
                        "ROMERO SNIPPET DEDUPLICATE: Ignorando duplicado ID=%s, Name=%s, CleanName=%s",
                        rec.id, rec.name, name_key,
                    )
            records = filtered
        return super()._filter_records_to_values(records, is_sample)
