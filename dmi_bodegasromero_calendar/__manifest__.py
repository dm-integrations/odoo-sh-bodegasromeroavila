# Copyright 2024 Dmintegrations.eu (http://www.dmintegrations.eu)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    'name': 'DMI Bodegas Romero Base',
    'version': '17.0.1.0.4',
    'category': 'Contacts',
    'summary': 'Personalizaciones para Bodegas Romero',
    'description': """
        En este modulo se desarrollan personalizaciones propiar para el cliente Bodegas Romero.
    """,
    "website": "https://dmintegrations.eu",
    "author": "Dm integrations",
    'depends': [
        'crm',
        'calendar',
        'web',
    ],
    'data': [
        'views/calendar_event_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            # 'dmi_bodegasromero_calendar/static/src/js/*',
            'dmi_bodegasromero_calendar/static/src/views/**/*',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'OPL-1',
}
