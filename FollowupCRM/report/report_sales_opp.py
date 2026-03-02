# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt Ltd.
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
 
class CRMOpportunityActivity(models.AbstractModel):
    _name = "report.print_crm_opportunity_activity.report_sales_opp"

   

    @api.model
    # def render_html(self, docids, data=None):
    def _get_report_values(self, docids, data=None):  # odoo 11
        report = self.env['ir.actions.report']._get_report_from_name(
            'print_crm_opportunity_activity.report_sales_opp')
        opportunity = self.env['crm.lead'].browse(docids)
        # docargs = {
        return {
            'doc_model': 'crm.lead',
            'data': data,
            'docs': self.env['crm.lead'].browse(docids)
        }
            s.custom_stage_id"""
        return res        
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: