from odoo import models, fields

class CrmLeadInherit(models.Model):
    _inherit = 'crm.lead'

    service = fields.Many2many(
        'product.product', string='Services',
        help='Select services related to this lead.'
    
    )

    lead_issue = fields.Char(string="Issue")
    proposal_date = fields.Date(string="Proposal Expected")
   