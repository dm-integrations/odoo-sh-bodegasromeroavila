# Copyright 2024 Dmintegrations.eu (http://www.dmintegrations.eu)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    'name': 'DMI Bodegas Romero Informes',
    'version': '17.0.1.0.0',
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
    ],
    'data': [ 
        'views/base_document_layout_views.xml',
        'views/report_templates_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'OPL-1',
}
