from odoo import fields, models, api

class CustomCrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.model
    def search_by_contact_group(self, contact_group_id):
        domain = [('contact_group_ids', 'in', [contact_group_id])]
        return self.search(domain)

# Modify the crm.lead model to include the Many2Many field
class Lead(models.Model):
    _inherit = 'crm.lead'

    contact_group_ids = fields.Many2many(
        'res.partner.contactgroups',  # Use the existing model name
        string='Contact Groups',
        relation='crm_lead_contact_group_rel',
        column1='lead_id',
        column2='contact_group_id'
    )