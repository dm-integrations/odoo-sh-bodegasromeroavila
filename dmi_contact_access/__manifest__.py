{
    'name': 'DMI Contact Access',
    'version': '17.0.1.1.2',
    'category': 'Contacts',
    'summary': 'Restricts access to contacts based on the assigned salesperson',
    'description': """
        This module restricts internal users' access to contacts.
    Users can see and use a contact only if they are assigned as the salesperson on the res.partner form.
    """,
    'depends': ['base', 'contacts', 'sale_management'],
    'data': [
        'security/contact_access_rules.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'OPL-1',
}
