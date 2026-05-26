# Copyright 2024 Dmintegrations.eu (http://www.dmintegrations.eu)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    'name': 'DMI Bodegas Romero Informes',
    'version': '17.0.1.0.3',
    'category': 'Reports',
    'summary': 'Personalizaciones Informes para Bodegas Romero',
    'description': """
        En este modulo se desarrollan personalizaciones de informes propias de el cliente Bodegas Romero.
    """,
    "website": "https://dmintegrations.eu",
    "author": "Dm integrations",
    'depends': [
        'base',
        'web',
        'point_of_sale',
        'dmi_bodegasromero_base',
    ],
    'data': [ 
        'views/pos_assets_index_views.xml',
        'views/base_document_layout_views.xml',
        'views/account_move_views.xml',
        'reports/report_sale_order_views.xml',
        'reports/report_invoice_views.xml',
        'views/report_templates_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'dmi_bodegasromero_reports/static/src/overrides/order_receipt.xml',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'OPL-1',
}
