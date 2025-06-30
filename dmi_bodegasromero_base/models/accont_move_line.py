from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    dmi_grados = fields.Float(string='Grados')

    dmi_alcohol_grados_discount = fields.Float(
        string="Grados Discount %",
        compute="_compute_alcohol_grados_discount",
        store=True,
        digits=(16, 2),
    )

    @api.depends('dmi_grados')
    def _compute_alcohol_grados_discount(self):
        for line in self:
            line.dmi_alcohol_grados_discount = 100 * (1 - line.dmi_grados / 100) if line.dmi_grados else 0.0

    def _get_effective_discount(self):
        """
        Calculate the combined discount from standard discount and dmi_grados.
        """
        self.ensure_one()
        if self.dmi_grados > 0 and self.dmi_grados < 100:
            price_multiplier_discount = 1.0 - (self.discount / 100.0)
            price_multiplier_grados = self.dmi_grados / 100.0
            effective_discount = 100.0 * (1.0 - (price_multiplier_discount * price_multiplier_grados))
            return effective_discount
        return self.discount

    @api.depends('quantity', 'discount', 'price_unit', 'tax_ids', 'currency_id', 'dmi_grados')
    def _compute_totals(self):
        """
        Compute on-screen totals for the invoice line, accounting for both discount and dmi_grados.
        """
        super()._compute_totals()
        for line in self.filtered(lambda l: l.display_type == 'product' and l.dmi_grados):
            price_after_discount = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            final_price_unit = price_after_discount * (line.dmi_grados / 100.0)
            _logger.info("Computing totals for invoice line %s: final_price_unit=%s, quantity=%s, taxes=%s",
                         line.id, final_price_unit, line.quantity, line.tax_ids)
            if line.tax_ids:
                taxes_res = line.tax_ids.compute_all(
                    price_unit=final_price_unit,
                    quantity=line.quantity,
                    currency=line.currency_id,
                    product=line.product_id,
                    partner=line.move_id.partner_id,
                    is_refund=line.is_refund,
                )
                line.price_subtotal = taxes_res['total_excluded']
                line.price_total = taxes_res['total_included']
            else:
                line.price_total = line.price_subtotal = final_price_unit * line.quantity

    def _convert_to_tax_base_line_dict(self):
        """
        Prepare data for tax summary widget and journal entry creation, using effective discount.
        """
        self.ensure_one()
        is_invoice = self.move_id.is_invoice(include_receipts=True)
        sign = -1 if self.move_id.is_inbound(include_receipts=True) else 1
        effective_discount = self._get_effective_discount()
        return self.env['account.tax']._convert_to_tax_base_line_dict(
            self,
            partner=self.partner_id,
            currency=self.currency_id,
            product=self.product_id,
            taxes=self.tax_ids,
            price_unit=self.price_unit if is_invoice else self.amount_currency,
            quantity=self.quantity if is_invoice else 1.0,
            discount=effective_discount,
            account=self.account_id,
            analytic_distribution=self.analytic_distribution,
            price_subtotal=sign * self.amount_currency,
            is_refund=self.is_refund,
            rate=(abs(self.amount_currency) / abs(self.balance)) if self.balance else 1.0
        )

    def _convert_to_tax_line_dict(self):
        """
        Convert the current record to a dictionary for tax computation, ensuring correct tax amount.
        """
        self.ensure_one()
        sign = -1 if self.move_id.is_inbound(include_receipts=True) else 1
        product_line = self.move_id.invoice_line_ids.filtered(
            lambda l: l.display_type == 'product' and l.id != self.id
        )[:1]  # Take the first record to avoid multi-record issues
        dmi_grados = product_line.dmi_grados if product_line else self.dmi_grados
        if len(product_line) > 1:
            _logger.warning(
                "Multiple product lines found for tax line %s. Using the first one (ID: %s).",
                self.id, product_line[0].id if product_line else "none"
            )
        taxes = self.tax_ids or product_line.tax_ids
        _logger.info(
            "Tax line for invoice line %s: amount_currency=%s, dmi_grados=%s, taxes=%s",
            self.id, self.amount_currency, dmi_grados, taxes
        )
        tax_amount_value = (sign * self.amount_currency) / 10 if dmi_grados else sign * self.amount_currency
        return self.env['account.tax']._convert_to_tax_line_dict(
            self,
            partner=self.partner_id,
            currency=self.currency_id,
            taxes=taxes,
            tax_tags=self.tax_tag_ids,
            tax_repartition_line=self.tax_repartition_line_id,
            group_tax=self.group_tax_id,
            account=self.account_id,
            analytic_distribution=self.analytic_distribution,
            tax_amount=tax_amount_value,
        )