# Copyright 2024 Dmintegrations.eu (http://www.dmintegrations.eu)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    'name': 'DMI Bodegas Romero Informes',
    'version': '17.0.1.0.5',
    'category': 'Contacts',
    'summary': 'Personalizaciones para Bodegas Romero',
    'description': """
        En este modulo se desarrollan personalizaciones propiar para el cliente Bodegas Romero.
    """,
    "website": "https://dmintegrations.eu",
    "author": "Dm integrations",
    'depends': [
        'dmi_bodegasromero_base',
    ],
    'data': [
        'reports/account_invoice_report.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'OPL-1',
}
