# -*- coding: utf-8 -*-
# (c) 2025 Nexta - Jaume Basiero <jbasiero@nextads.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/a
from odoo import fields, models


class Website(models.Model):
    _inherit = 'website'

    mail_template_id = fields.Many2one(comodel_name="mail.template", string="Mail Template")