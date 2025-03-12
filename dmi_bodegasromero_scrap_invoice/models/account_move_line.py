from odoo import models, api, fields, _


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def get_info_components(self):
        if not self.product_id or not self.product_id.product_template_component_ids:
            return False

        total = 0
        total_qty = 0
        total_quote = 0

        for component in self.product_id.product_template_component_ids:
            total += self.quantity * component.quote
            total_qty += self.quantity
            total_quote += component.quote
        return {
            'total': total,
            'total_qty': total_qty,
            'total_quote': total_quote
        }