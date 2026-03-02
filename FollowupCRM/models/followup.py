from odoo import fields, models

class ShippingInvoice(models.Model):
    _inherit = 'crm.lead'
    order_line = fields.One2many('followup.followup', 'shipping_invoice_id', string='Order Lines')


class Followup(models.Model):
    _name = 'followup.followup'
    _description = 'Follow-up Log'

    date = fields.Date(string='تاريخ المتابعة', default=fields.Date.today(), required=True)
    method = fields.Char(string='طريقة التواصل', required=True)
    result = fields.Char(string='نتيجة التواصل', required=True)
    shipping_invoice_id = fields.Many2one('crm.lead', string='Shipping Invoice')
