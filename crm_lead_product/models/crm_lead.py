# Copyright (C) 2017-2024 ForgeFlow S.L. (https://www.forgeflow.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

from odoo import api, fields, models, Command, _
from odoo.exceptions import UserError

class CrmLead(models.Model):
    _inherit = "crm.lead"

    lead_line_ids = fields.One2many(
        comodel_name="crm.lead.line", 
        inverse_name="lead_id", 
        string="Lead Lines"
    )

    @api.onchange("lead_line_ids")
    def _onchange_lead_line_ids(self):
        expected_revenue = 0
        for lead_line in self.lead_line_ids:
            expected_revenue += lead_line.expected_revenue
        self.expected_revenue = expected_revenue

    def action_make_quotation(self):
        self.ensure_one()
        if not self.partner_id:
            raise UserError(_("Please set a customer before creating a quotation."))
        if not self.lead_line_ids:
            raise UserError(_("Please add at least one product line."))

        # Create Sale Order lines from Lead lines
        order_lines = []
        for line in self.lead_line_ids:
            order_lines.append(Command.create({
                'product_id': line.product_id.id,
                'name': line.name,
                'product_uom_qty': line.product_qty,
                'product_uom': line.uom_id.id,
                'price_unit': line.price_unit,
            }))

        # Create the Sale Order
        # opportunity_id link ensures it shows up in the standard Odoo Smart Button
        sale_order = self.env['sale.order'].create({
            'partner_id': self.partner_id.id,
            'opportunity_id': self.id,
            'team_id': self.team_id.id,
            'campaign_id': self.campaign_id.id,
            'medium_id': self.medium_id.id,
            'source_id': self.source_id.id,
            'order_line': order_lines,
        })

        return {
            'name': _('Quotation'),
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'res_id': sale_order.id,
            'target': 'current',
        }