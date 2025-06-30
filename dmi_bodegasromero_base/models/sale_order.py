from odoo import models, api, fields, _
import base64
import json


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        self.with_user(1).action_open_reward_wizard()
        return super().action_confirm()

    def _get_program_domain(self):
        res = super()._get_program_domain()
        res.append('|')
        res.append(('partner_ids', 'in', self.partner_id.ids))
        res.append(('partner_ids', 'in', self.partner_id.ids))
        return res
