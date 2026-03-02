from odoo import api, fields, models, _
from datetime import date, datetime, timedelta


class CrmLead(models.Model):
    _inherit = "crm.lead"

    due_date = fields.Datetime(string='Due Date')
    current_date = fields.Datetime(string='Current Date', default=fields.Date.today())
    due = fields.Boolean(string='Due', default=False)

    @api.onchange('due_date')
    def change_due_date_color(self):
        if self.due_date:
            if self.due_date <= self.current_date:
                self.due = True
            else:
                self.due = False
        else:
            self.due = False
