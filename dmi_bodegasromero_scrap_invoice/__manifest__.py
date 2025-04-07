# Copyright 2024 Dmintegrations.eu (http://www.dmintegrations.eu)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    'name': 'DMI Bodegas Romero Scrap Invoice',
    'version': '17.0.1.0.3',
    'category': 'Contacts',
    'summary': 'DMI Bodegas Romero Scrap Invoice',
    'description': """
        Este módulo permite mostar en las facturas la contribución al SCRAP de forma desglosada.
    """,
    "website": "https://dmintegrations.eu",
    "author": "Dm integrations",
    'depends': [
        'base',
        'account',
        'product',
        'stock',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/precision_data.xml',
        'reports/report_invoice.xml',
        'views/product_component_views.xml',
        'views/product_template_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'OPL-1',
}
