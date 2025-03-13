# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools


class BaseDocumentLayout(models.TransientModel):
    _inherit = 'base.document.layout'

    dmi_report_terms_and_conditions = fields.Html(
        string='Términos y condiciones',
        help='Términos y condiciones que se mostrarán en los informes.',
        translate=True,
        related='company_id.dmi_report_terms_and_conditions', readonly=False
    )
