# Copyright 2024 Dmintegrations.eu (http://www.dmintegrations.eu)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    'name': 'DMI Bodegas Romero Base',
    'version': '17.0.1.0.7',
    'category': 'Contacts',
    'summary': 'Personalizaciones para Bodegas Romero',
    'description': """
        En este modulo se desarrollan personalizaciones propiar para el cliente Bodegas Romero.
    """,
    "website": "https://dmintegrations.eu",
    "author": "Dm integrations",
    'depends': [
        'hr',
        'mail',
        'spreadsheet_dashboard',
        'website',
        'crm',
        'sms',
        'sale_management',
        'sale_loyalty',
        'product',
        'l10n_es_edi_facturae',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron_data.xml',
        'data/crm_lead_fuente_data.xml',
        'views/crm_lead_views.xml',
        'views/crm_lead_fuente_views.xml',
        'views/product_pricelist_views.xml',
        'views/res_partner_views.xml',
        'views/res_partner_category_views.xml',
        'views/sale_order_views.xml',
        'views/loyalty_views.xml',
        'views/project_task_views.xml',
        'views/menu_views.xml',
        'views/mail_templates.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'OPL-1',
}
