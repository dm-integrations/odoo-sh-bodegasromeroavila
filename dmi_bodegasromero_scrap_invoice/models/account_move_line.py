from odoo import models, api, fields, _


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def get_info_components(self):
        if not self.product_id or not self.product_id.product_template_component_ids:
            return False

        total = 0
        total_quote = 0
        total_quantity = self.quantity
        for component in self.product_id.product_template_component_ids:
            total += self.quantity * component.quote
            total_quote += component.quote
        return {
            'total': total,
            'total_quantity': total_quantity,
            'total_quote': total_quote
        }

    def get_info_components_resume(self):
        if not self.product_id or not self.product_id.product_template_component_ids:
            return False

        vals = []

        for component in self.product_id.product_template_component_ids:
            vals.append({
                'name': component.product_component_id.name,
                'quantity': self.quantity,
                'price_unit': component.price_unit,
                'price_weight': component.price_weight,
                'weight': component.weight,
                'total_quote': round(self.quantity * component.quote, 5)
            })
        return vals
