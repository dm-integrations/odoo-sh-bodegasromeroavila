from odoo import models, api, fields, _
from odoo.exceptions import UserError


class CrmLeadFuente(models.Model):
    _name = "crm.lead.fuente"
    _description = "crm_lead_fuente"

    name = fields.Char(
        string="Fuente",
        required=True
    )

    def unlink(self):
        if self.id == 1:
            raise UserError(_("No se puede eliminar la fuente por defecto"))
        return super(CrmLeadFuente, self).unlink()
