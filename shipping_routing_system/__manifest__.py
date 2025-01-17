# -*- coding: utf-8 -*-
{
    'name': 'Shipping Routing Module',
    'version': '1.0.0',
    'summary': 'Select carrier module',
    'description': 'This module selects the best option in a carriers list.',
    'author': '"Sergio Guerrero"',
    'depends': ['base', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_extension_views.xml',
        'views/sale_order_shipping_option_view.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'your_module_name/static/src/css/styles.css',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
