# -*- coding: utf-8 -*-
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request


class DmiWebsiteSale(WebsiteSale):

    def _shop_lookup_products(self, attrib_set, options, post, search, website):
        fuzzy_search_term, product_count, search_result = super()._shop_lookup_products(
            attrib_set, options, post, search, website
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
