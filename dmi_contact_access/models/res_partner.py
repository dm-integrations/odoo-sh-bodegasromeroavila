from odoo import models, api, fields, _


class ResPartner(models.Model):
    _inherit = "res.partner"

    internal_partner = fields.Boolean(
        string="Es cliente interno",
        default=False,
        compute="_compute_is_internal_partner",
        store=True,
    )

    @api.depends("user_id", "user_ids")
    def _compute_is_internal_partner(self):
        user_obj = self.env["res.users"]
        for record in self:
            partner_id = user_obj.search([("partner_id", "=", record.id)], limit=1)
            record.internal_partner = True if partner_id else False
