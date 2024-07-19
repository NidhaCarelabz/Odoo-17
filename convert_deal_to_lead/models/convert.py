from odoo import models, fields 

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def action_convert_to_lead(self):
        for lead in self:
            if lead.type == 'opportunity':
                # Try to find the 'Assigned' stage using the XML ID
                try:
                    assigned_stage = self.env.ref('lead_stages.crm_lead_stage_second')
                except ValueError:
                    # Fallback to search by name and sequence if XML ID is not found
                    assigned_stage = self.env['crm.stage'].search([('name', '=', 'Assigned'), ('sequence', '=', 5)], limit=1)
                
                if not assigned_stage:
                    raise ValueError("The 'Assigned' stage does not exist. Please check your CRM stages.")
                
                # Ensure the 'Deal back Lead' tag exists
                tag = self.env['crm.tag'].search([('name', '=', 'Deal back Lead')], limit=1)
                if not tag:
                    tag = self.env['crm.tag'].create({'name': 'Deal back Lead'})
                
                # Add the tag to the lead
                lead.tag_ids = [(4, tag.id)]

                # Update lead type to 'lead' and move to the 'Assigned' stage
                lead.write({
                    'type': 'lead',
                    'stage_id': assigned_stage.id,
                    'active': True  # Ensure the lead remains active
                })

                # Post a message to indicate the conversion
                lead.message_post(body="Opportunity converted to lead and moved to the 'Assigned' stage.")
        
        return True
