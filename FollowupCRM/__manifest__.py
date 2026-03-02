# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'CRM Form Follow-up',
    'version': '16.0.0.1',
    'category': 'Sales',
    'license': 'OPL-1',
    'summary': 'This plugin helps to follow-up and managing customer',
    'description': "provides a customer follow-up feature in managing customer relations by facilitating communication. ",
    'author': "Pure IT Solutions",
    'depends': ['crm','sale','sale_management'],
    'data': [
        'views/followup_views.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    "images":["static/description/odoo-CRM-sales.png"],
}
