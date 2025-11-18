{
    'name': 'Croissantage',
    "version": "19.0.0.0.1",
    'category': 'Human Resources/Lunch',
    'website': 'https://www.odoo.com/',
    'summary': 'Allows to manage croissantages within your company.',
    'description': """Allows to manage croissantages within your company.""",
    'depends': [
        'contacts',
    ],
    'data': [
        'views/croissantage_event.xml',
        'views/res_partner.xml'
    ],
    'demo': [
        'demo/croissantage_event_demo.xml',
    ],
    'installable': True,
    'auto_install': True,
    'application': True,
    'author': 'Odoo LU S.A.',
    'license': 'LGPL-3',
}
