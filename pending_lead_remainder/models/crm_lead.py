# -*- coding: utf-8 -*-
from importlib._common import _
from markupsafe import Markup

from odoo import models, fields, api
from datetime import datetime, timedelta


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def check_pending_leads(self):
        # Calculate the date X days ago from today
        date_limit = datetime.now() - timedelta(days=10)

        # Find the first stage (stage with the lowest sequence number)
        first_stage = self.env['crm.stage'].search([], order='sequence', limit=1)
        first_stage_id = first_stage.id if first_stage else False

        # Search for leads that are in first stage and created before the date limit
        pending_leads = self.env['crm.lead'].search([
            ('stage_id', '=', first_stage_id),
            ('date_open', '<=', date_limit),
            ('type', '=', 'lead')
        ])

        # Search for opportunity that are in first stage and created before the date limit
        opportunity_leads = self.env['crm.lead'].search([
            ('stage_id', '=', first_stage_id),
            ('date_open', '<=', date_limit),
            ('type', '=', 'opportunity')
        ])

        all_leads = pending_leads + opportunity_leads

        rec_by_salesperson = {}
        for rec in all_leads:
            if rec.user_id:
                salesperson = rec.user_id.partner_id
                if salesperson not in rec_by_salesperson:
                    rec_by_salesperson[salesperson] = []
                rec_by_salesperson[salesperson].append(rec)

        # Create a message for each salesperson for pending leads
        for salesperson, data in rec_by_salesperson.items():
            message_body = Markup("<p>Dear {salesperson_name},</p>").format(salesperson_name=salesperson.name)
            message_body += Markup(
                "<p>The following leads/opportunities are still in the initial stage. Please review and take the necessary action:</p>")
            message_body += Markup("<ul>")
            for rec in data:
                message_body += Markup("<li> '{rec_name}' is a {rec_type} that was created on {rec_date}.</li>").format(
                    rec_name=rec.name,
                    rec_type=rec.type,
                    rec_date=rec.create_date.strftime('%Y-%m-%d')
                )
            message_body += Markup("</ul>")

            # Get or create the discuss channel for the salesperson
            channel = self.env['discuss.channel'].channel_get([salesperson.id])

            # Post the message to the channel
            if channel:
                channel.message_post(body=message_body, message_type='comment', subtype_xmlid="mail.mt_comment")

