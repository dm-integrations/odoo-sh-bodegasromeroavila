from odoo import models, api, fields, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    def action_post(self):
        if not self.partner_id.vat:
            raise UserError(_('El NIF del cliente no es correcto. Por favor verifique el NIF del cliente.'))

        return super(AccountMove, self).action_post()


