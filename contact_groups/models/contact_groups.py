# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, api

class ContactGroups(models.Model):
    _name = "res.partner.contactgroups"
    _description = "Contact Groups"
    _rec_name = 'contact_group_name'
    _groups = 'contact_groups'

    contact_group_name = fields.Char('Group Name', required=True, translate=True)
    contact_groups = fields.Many2many(
        'res.partner',
        string="Contact Groups",
        required=True,
        context={'default_contact_groups_id': lambda self: self.id},
    )

    @api.model  # Decorator to mark as a model method
    def create(self, vals):
        # Remove the potentially problematic `default_contact_groups_id` context
        if 'context' in vals and 'default_contact_groups_id' in vals['context']:
            del vals['context']['default_contact_groups_id']

        return super(ContactGroups, self).create(vals)