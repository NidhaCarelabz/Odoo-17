# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, api

class Lead(models.Model):
    _inherit = 'crm.lead'

    lead_stage_id = fields.Many2one(
        'crm.lead.stage', string='Stage', index=True, tracking=True, readonly=False, group_expand='_default_lead_stage')

    @api.model
    def _default_lead_stage(self, stages, domain, order):
        return self.env['crm.lead.stage'].search([])

    def write(self, vals):
        if 'user_id' in vals and self.lead_stage_id.name == 'Open':
            assigned_stage = self.env['crm.lead.stage'].search([('name', '=', 'Assigned')], limit=1)
            if assigned_stage:
                vals['lead_stage_id'] = assigned_stage.id
        return super(Lead, self).write(vals)






