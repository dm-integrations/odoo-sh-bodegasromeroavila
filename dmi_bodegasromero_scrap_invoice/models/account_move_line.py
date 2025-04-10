from odoo import models, api, fields, _


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def get_info_components(self):

        if not self.product_id or not self.product_id.product_template_component_ids:
            return False
        is_packaging = any(self.mapped("sale_line_ids.product_packaging_id"))
        total = 0
        total_quote = 0
        total_quantity = self.quantity
        product_components = self.product_id.product_template_component_ids.filtered(
            lambda x: not x.exclude_not_packaging) if not is_packaging else self.product_id.product_template_component_ids
        for component in product_components:
            total += self.quantity * component.quote
            total_quote += component.quote
        return {
            'total': round(total, 7),
            'total_quantity': total_quantity,
            'total_quote': round(total_quote, 7)
        }

    def get_info_components_resume(self):
        if not self.product_id or not self.product_id.product_template_component_ids:
            return False

        is_packaging = any(self.mapped("sale_line_ids.product_packaging_id"))
        vals = []

        product_components = self.product_id.product_template_component_ids.filtered(
            lambda x: not x.exclude_not_packaging) if not is_packaging else self.product_id.product_template_component_ids

        for component in product_components:
            vals.append({
                'name': component.product_component_id.name,
                'quantity': self.quantity,
                'price_unit': component.price_unit,
                'price_weight': component.price_weight,
                'weight': component.weight,
                'total_quote': round(self.quantity * component.quote, 7)
            })
        return vals
