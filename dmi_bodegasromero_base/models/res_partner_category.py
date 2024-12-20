from odoo import models, api, fields, _


class PartnerCategory(models.Model):
    _inherit = 'res.partner.category'
    _order = 'sequence, name'

    sequence = fields.Integer('Sequence', default=10)
