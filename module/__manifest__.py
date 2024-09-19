{
    'name': 'My Demo Module',
    "version": "17.0.0.0.1",
    'website': 'https://www.odoo.com/',
    'summary': 'Demo.',
    'description': """Demo for your company.""",
    'depends': [
        'contacts',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/croissantage.xml',
        'views/res_partner.xml'
    ],
    'installable': True,
    'auto_install': True,
    'application': True,
    'license': 'LGPL-3',
}
