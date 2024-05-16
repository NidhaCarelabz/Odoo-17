from odoo import models, fields

class CrmLeadInherit(models.Model):
    _inherit = 'crm.lead'

    x_contact_medium = fields.Char(string="Contact Medium")

    service = fields.Many2many(
        'product.product', string='Services',
        help='Select services related to this lead.'
    
    )

    lead_source = fields.Selection([
                        ('web_form', 'Web Form'),
                        ('cold_call', 'Cold Call'),
                        ('referral', 'Referral'),
                        ('email_campaign', 'Email Campaign'),
                        ('social_media', 'Social Media'),
                        ('trade_show', 'Trade Show'),
                        ('online_advertising', 'Online Advertising'),
                        ('content_marketing', 'Content Marketing'),
                        ('seo', 'Search Engine Optimization (SEO)'),
                        ('word_of_mouth', 'Word of Mouth'),
                        ('partner_programs', 'Partner Programs'),
                        ('inbound_marketing', 'Inbound Marketing'),
                        ('direct_mail', 'Direct Mail'),
                        ('television_or_radio_advertising', 'Television or Radio Advertising'),
                        ('print_advertising', 'Print Advertising'),
                        ('event_marketing', 'Event Marketing'),
                        ('networking', 'Networking'),
                        ('online_communities', 'Online Communities'),
                        ('customer_referrals', 'Customer Referrals'),
                        ('other', 'Other')
                        ], string='Sources', help='Select the lead source')

    lead_issue = fields.Char(string="Issue")
    proposal_date = fields.Date(string="Proposal Expected")