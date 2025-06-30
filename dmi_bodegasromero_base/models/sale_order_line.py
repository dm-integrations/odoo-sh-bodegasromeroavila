from odoo import models, fields, api, _

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_image = fields.Image(
        string='Imagen',
        related='product_id.image_128',
    )

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

    def _convert_to_tax_base_line_dict(self, **kwargs):
        self.ensure_one()

        # Combine grados with existing discount to compute an effective discount
        if self.dmi_grados:
            effective_discount = 100 * (1 - ((self.dmi_grados / 100.0) * (1 - self.discount / 100.0)))
        else:
            effective_discount = self.discount
        return self.env['account.tax']._convert_to_tax_base_line_dict(
            self,
            partner=self.order_id.partner_id,
            currency=self.order_id.currency_id,
            product=self.product_id,
            taxes=self.tax_id,
            price_unit=self.price_unit,
            quantity=self.product_uom_qty,
            discount=effective_discount,
            price_subtotal=self.price_subtotal,
            **kwargs
        )

    def _prepare_invoice_line(self, **optional_values):
        vals = super()._prepare_invoice_line(**optional_values)
        vals['dmi_grados'] = self.dmi_grados
        return vals
