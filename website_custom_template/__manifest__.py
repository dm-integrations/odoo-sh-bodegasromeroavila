# -*- coding: utf-8 -*-
# (c) 2025 Nexta - Jaume Basiero <jbasiero@nextads.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/a
{
    'name': "Website custom mail template",
    'summary': """Este modulo modifica las plantillas de correo para cada compañia al confirma un pedido en el website""",
    'description': """Este modulo modifica las plantillas de correo para cada compañia al confirma un pedido en el website""",
    'author': "NextaDS",
    'website': "https://www.nextads.es",
    'category': '',
    'version': '17.0.0.2',
    'license': "LGPL-3",
    'depends': [
        'website',
        'sale',
    ],

    'data': [
        'views/website_views.xml',
    ],

    'installable': True
}