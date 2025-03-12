import logging

from odoo import _, api, fields, models, SUPERUSER_ID
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class AccountMoveSend(models.TransientModel):
    _inherit = 'account.move.send'

    l10n_es_edi_facturae_checkbox_xml = fields.Boolean(
        string="Generate Facturae edi file",
        default=False,
        company_dependent=True,
    )
