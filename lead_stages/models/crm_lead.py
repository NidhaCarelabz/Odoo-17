from odoo import fields, models, api

class Lead(models.Model):
    _inherit = 'crm.lead'

    def _default_stage_open(self):
        open_stage = self.env['crm.lead.stage'].search([('name', '=', 'Open')], limit=1)
        return open_stage.id if open_stage else None

    lead_stage_id = fields.Many2one(
        'crm.lead.stage', string='Stage', index=True, tracking=True, readonly=False, default=_default_stage_open, group_expand='_group_expand_lead_stage')

    @api.model
    def _group_expand_lead_stage(self, stages, domain, order):
        # Return all stages for group expand
        return self.env['crm.lead.stage'].search([])

    def write(self, vals):
        if 'user_id' in vals and self.lead_stage_id.name == 'Open':
            assigned_stage = self.env['crm.lead.stage'].search([('name', '=', 'Assigned')], limit=1)
            if assigned_stage:
                vals['lead_stage_id'] = assigned_stage.id
        return super(Lead, self).write(vals)
