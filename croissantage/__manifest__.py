{
    'name': 'Croissantage',
    "version": "19.0.0.0.1",
    'category': 'Human Resources/Lunch',
    'website': 'https://www.odoo.com/',
    'summary': 'Allows to manage croissantages within your company.',
    'description': """Allows to manage croissantages within your company.""",
    'depends': [
        'contacts',
        'website'
    ],
    'data': [
        'security/croissantage_security.xml',
        'security/ir.model.access.csv',
        'views/croissantage_event.xml',
        'views/res_partner.xml',
        'views/croissantage_page.xml',
    ],
    'demo': [
        'demo/croissantage_event_demo.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'croissantage/static/src/js/croissantage_filter.js',
            'croissantage/static/src/scss/style.scss',
        ],
    },
    'installable': True,
    'auto_install': True,
    'application': True,
    'author': 'Odoo LU S.A.',
    'license': 'LGPL-3',
}
