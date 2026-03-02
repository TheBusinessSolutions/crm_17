# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name" : "Pipeline Product to Sales Order | CRM Product to Quotation",
    "version" : "17.0.0.0",
    "category" : "Sales",
    'summary': 'Pipeline Product to Quotation CRM Product to Sales Order CRM Product to Sale Order add products on pipeline to quotation add product on pipeline to sales order product from lead add product on lead to quotation add product on crm pipeline to quote product',
    "description": """
       CRM Product to Quotation Odoo App helps users to easily create, manage, and track quotation directly from the pipeline view. This app integrates seamlessly with the CRM, allowing users to add multiple product to lead or pipeline, and create sales quotation directly from the CRM. This makes it easy to create accurate and detailed quotation that are tailored to the specific needs of each customer. In addition, the app allows users to track the quotation from CRM using smart buttons.
    """,
    "author": "BROWSEINFO",
    'website': 'https://www.browseinfo.com/demo-request?app=bi_crm_product_quotation&version=17&edition=Community',
    "depends" : ['base','crm','product','account','sale_management','sale_crm'],
    "data": [
          'security/ir.model.access.csv',
          'views/crm_lead_inherit.xml',
          'views/sale_crm_view.xml',          
    ],
    "license":'OPL-1',
    "auto_install": False,
    "installable": True,
    "live_test_url":'https://www.browseinfo.com/demo-request?app=bi_crm_product_quotation&version=17&edition=Community',
    "images":['static/description/Banner.gif'],
}

