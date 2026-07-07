# -*- coding: utf-8 -*-
# (c) 2025 Nexta - Jaume Basiero <jbasiero@nextads.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/a
from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _get_confirmation_template(self):
        res = super()._get_confirmation_template()
        if self.website_id and self.website_id.mail_template_id:
            res = self.website_id.mail_template_id
        return res