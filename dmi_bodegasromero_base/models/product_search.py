# -*- coding: utf-8 -*-
import logging
from odoo import models, api, fields

_logger = logging.getLogger(__name__)


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

    @api.model
    def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
        """
        Sobrescribimos el _search de bajo nivel del modelo product.product.
        Si la petición HTTP proviene de la tienda web (ruta que comienza por '/shop'),
        e intentan buscar variantes de producto generales, agrupamos los resultados por plantilla de producto
        para que figure un único anuncio representativo por cada plantilla física, impidiendo listas duplicadas en la tienda.
        """
        res = super(ProductProduct, self)._search(domain, offset=offset, limit=limit, order=order, access_rights_uid=access_rights_uid)
        
        try:
            from odoo.http import request
            # Solo aplicamos el filtro si estamos en una petición de la web corporativa en '/shop'
            if request and request.httprequest and request.httprequest.path.startswith('/shop'):
                # Evitamos filtrar si se está buscando por IDs específicos de variante (por ejemplo al añadir al carrito, checkout o ficha técnica)
                has_specific_id_filter = False
                for dom in domain:
                    if isinstance(dom, (list, tuple)) and dom[0] in ('id', 'product_variant_ids', 'product_variant_id'):
                        has_specific_id_filter = True
                        break
                        
                if not has_specific_id_filter and res:
                    # Agrupamos por product_tmpl_id y guardamos solo una variante por cada plantilla física
                    records = self.browse(res)
                    seen_templates = set()
                    filtered_ids = []
                    for rec in records:
                        tmpl_id = rec.product_tmpl_id.id
                        if tmpl_id not in seen_templates:
                            seen_templates.add(tmpl_id)
                            filtered_ids.append(rec.id)
                    # El resultado de la búsqueda debe ser un id entero o lista de ids
                    if isinstance(res, list):
                        res = filtered_ids
                    else:
                        # Si `res` no es una lista directa, lo devolvemos como lista filtrada para mayor seguridad
                        res = filtered_ids
        except Exception as e:
            _logger.error("Error aplicando agrupacion de variantes por plantilla en _search en el e-commerce: %s", str(e))
            
        return res
