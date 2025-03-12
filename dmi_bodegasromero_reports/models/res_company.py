# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools


class ResCompany(models.Model):

    _inherit = 'res.company'

    dmi_report_terms_and_conditions = fields.Html(
        string='Términos y condiciones',
        help='Términos y condiciones que se mostrarán en los informes.',
    )
