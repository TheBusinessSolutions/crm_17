# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class crm_lead(models.Model):
    _inherit = 'crm.lead'

    lead_product_ids = fields.One2many('lead.line', 'lead_line_id', string='Products', copy=True)
    crm_count = fields.Integer(string="Quotation",compute="get_quotation_count")
    is_crm_quotation = fields.Boolean('Is CRM Quotation')

    def action_quotations_view(self):
        order_line = [] 
        for record in self.lead_product_ids:  
            order_line.append((0, 0, {
                                     'product_id'     : record.product_id.id,
                                     'name'           : record.name, 
                                     'product_uom_qty': record.product_uom_quantity,
                                     'price_unit'     : record.price_unit,
                                     'tax_id'        : [(6, 0, record.tax_id.ids)],
                                }))
        
        sale_obj = self.env['sale.order']
        if self.partner_id:
            for record in self.lead_product_ids:  
                if record.product_id and record.name:
                    sale_create_obj = sale_obj.create({
                                    'partner_id': self.partner_id.id,
                                    'opportunity_id': self.id,
                                    'state': "draft",
                                    'order_line': order_line,
                                    })
                return {
                    'name': "Sale Order",
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'sale.order',
                    'view_id': self.env.ref('sale.view_order_form').id,
                    'target': "new",
                    'res_id': sale_create_obj.id
                }
            else:
                raise UserError('Enter the "Product" and "Description".')
        else:
            raise UserError('Please select the "Customer".')             



    def open_quotation_from_view_action(self):
        action = self.env["ir.actions.actions"]._for_xml_id("sale.action_quotations_with_onboarding")
        action['domain'] = [('partner_id','=',self.partner_id.id),('opportunity_id','=',self.id)]
        return action


    def get_quotation_count(self):
        count = self.env['sale.order'].search_count([('partner_id','=',self.partner_id.id),('opportunity_id','=',self.id)])
        self.crm_count = count
