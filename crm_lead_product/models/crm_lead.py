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

    quotation_count = fields.Integer(
        string="Quotation Count",
        compute="_compute_quotation_count"
    )

    # -------------------------------------------------------------------------
    # Compute Methods
    # -------------------------------------------------------------------------

    def _compute_quotation_count(self):
        for lead in self:
            lead.quotation_count = self.env['sale.order'].search_count([
                ('opportunity_id', '=', lead.id)
            ])

    # -------------------------------------------------------------------------
    # Onchange Methods
    # -------------------------------------------------------------------------

    @api.onchange("lead_line_ids")
    def _onchange_lead_line_ids(self):
        expected_revenue = 0
        for lead_line in self.lead_line_ids:
            expected_revenue += lead_line.expected_revenue
        self.expected_revenue = expected_revenue

    # -------------------------------------------------------------------------
    # Override Methods
    # -------------------------------------------------------------------------

    def _convert_opportunity_data(self, customer, team_id=False):
        res = super()._convert_opportunity_data(customer, team_id)
        expected_revenue = 0
        for lead_line in self.lead_line_ids:
            expected_revenue += lead_line.expected_revenue
        res["expected_revenue"] = expected_revenue
        return res

    # -------------------------------------------------------------------------
    # Action Methods
    # -------------------------------------------------------------------------

    def action_create_quotation_from_lines(self):
        """Creates a Sale Order based on the Lead Lines."""
        self.ensure_one()

        if not self.partner_id:
            raise UserError(_("Please set a customer before creating a quotation."))

        if not self.lead_line_ids:
            raise UserError(_("Please add at least one product line before creating a quotation."))

        # Validate all lines have product and description
        for line in self.lead_line_ids:
            if not line.product_id or not line.name:
                raise UserError(_('Each line must have a "Product" and a "Description".'))

        # Map lead lines to sale order lines
        order_lines = []
        for line in self.lead_line_ids:
            product = line.product_id.with_context(
                lang=self.partner_id.lang,
                partner=self.partner_id,
                quantity=line.product_qty,
                pricelist=self.partner_id.property_product_pricelist.id
                if hasattr(self.partner_id, 'property_product_pricelist')
                and self.partner_id.property_product_pricelist else False,
                uom=line.uom_id.id or line.product_id.uom_id.id,
            )

            # Get taxes filtered by current company
            taxes = product.taxes_id.filtered(
                lambda t: t.company_id == self.env.company
            )

            line_vals = {
                'product_id': product.id,
                'name': line.name,
                'product_uom_qty': line.product_qty,
                'product_uom': line.uom_id.id or product.uom_id.id,
                'price_unit': line.price_unit,
                'tax_id': [Command.set(taxes.ids)],
            }

            order_lines.append(Command.create(line_vals))

        # Create the Sale Order linked to the opportunity
        sale_order = self.env['sale.order'].create({
            'partner_id': self.partner_id.id,
            'opportunity_id': self.id,
            'team_id': self.team_id.id,
            'campaign_id': self.campaign_id.id,
            'medium_id': self.medium_id.id,
            'source_id': self.source_id.id,
            'state': 'draft',
            'order_line': order_lines,
        })

        # Trigger product onchange on each line to populate
        # all missing fields like income account, etc.
        for sol in sale_order.order_line:
            sol._compute_tax_id()
            if hasattr(sol, 'product_id_change'):
                sol.product_id_change()
            if hasattr(sol, '_onchange_product_id'):
                sol._onchange_product_id()

        # Open the newly created quotation in a form view
        return {
            'name': _('Quotation'),
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'view_id': self.env.ref('sale.view_order_form').id,
            'res_id': sale_order.id,
            'target': 'current',
        }

    def action_view_quotations(self):
        """Opens the list of quotations linked to this opportunity."""
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "sale.action_quotations_with_onboarding"
        )
        action['domain'] = [('opportunity_id', '=', self.id)]
        action['context'] = {
            'default_opportunity_id': self.id,
            'default_partner_id': self.partner_id.id,
        }
        return action