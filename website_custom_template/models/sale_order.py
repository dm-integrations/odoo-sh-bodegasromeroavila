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

    def _send_payment_succeeded_for_order_mail(self):
        mail_template = super(SaleOrder, self)._send_payment_succeeded_for_order_mail()

        for order in self:
            if order.website_id and order.website_id.mail_template_id:
                mail_template = order.website_id.mail_template_id

            order._send_order_notification_mail(mail_template)