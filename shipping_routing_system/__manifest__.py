# -*- coding: utf-8 -*-
{
    'name': 'Shipping Routing Module',
    'version': '1.0.0',
    'summary': 'Select carrier module',
    'description': 'This module select the best option in a carriers list.',
    'author': '"Sergio Guerrero"',
    'depends': ['base',
                ],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_extension_views.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
