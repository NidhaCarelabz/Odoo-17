# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

import json
import logging
from datetime import datetime
import pytz


_logger = logging.getLogger(__name__)



class WebFormSalesEnquiry(http.Controller):
    @http.route('/contactus-salesenquiry',type='http', auth="public", website=True)
    def contactus_salesenquiry(self, **kw):
        country_ids = request.env['res.country'].sudo().search([])
        crm_services_ids = request.env['product.product'].sudo().search([])
        return request.render('web_form_sales_enquiry.contactus_salesenquiry', {'country_ids':country_ids,'crm_services_ids':crm_services_ids})

    @http.route('/contactus-salesenquiry/form/submit', type='http', auth="public", website=True)
    def contactus_salesenquiry_submit(self, **kw):
        if kw.get('web_sales_enq_country'):
            country_id = request.env['res.country'].sudo().search([('phone_code','=', int(kw.get('web_sales_enq_country')))])

        crm_services_ids_list = []
        if kw.get('web_sales_enq_services_vals'):
            crm_services_ids_list = [int(i) for i in kw.get('web_sales_enq_services_vals').split(',')]
        lead_stage_id = request.env['crm.lead.stage'].sudo().search([('sequence','=', 1)])
        lead_id = request.env['crm.lead'].sudo().create({
            'name': 'Quotation from ' + str(kw.get('web_sales_enq_comp_name')),
            'contact_name': kw.get('contact_name'),
            'email_from': kw.get('web_sales_enq_email'),
            'mobile': '+' + kw.get('web_sales_enq_country') + kw.get('web_sales_enq_mobile'),
            'description': kw.get('web_sales_enq_message'),
            'partner_name': kw.get('web_sales_enq_comp_name'),
            'country_id': country_id.id,
            'service': [(6, 0, crm_services_ids_list)],
            'lead_stage_id': lead_stage_id.id,
        })
        vals = {
            'lead_id': lead_id,
        }
        
        if kw.get('schedule_button'):
            return request.redirect('/contactus-salesenquiry/schedule-meeting?lead_id=%s' % (lead_id.id))
        elif kw.get('submit_button'):
            return request.render('web_form_sales_enquiry.sales_enquiry_contactus_thanks', vals)
    
    @http.route('/contactus-salesenquiry/schedule-meeting',type='http', auth='public',website = True)
    def contactus_salesenquiry_schedule_meeting(self, **kw):
        return request.render('web_form_sales_enquiry.crm_lead_schedule_meeting')
    
    @http.route('/contactus-salesenquiry/thank-you',type='http', auth='public',website = True)
    def contactus_salesenquiry_thanks(self, **kw):
        return request.render('web_form_sales_enquiry.sales_enquiry_contactus_thanks')

    @http.route('/schedule/meeting/submit', type='http', auth="public", methods=['POST'], website=True)
    def schedule_meeting(self, **post):
        lead_id = request.params.get('lead_id')

        if not lead_id:
            return request.redirect('/contactus-salesenquiry/thank-you')
        else:
            lead_id = request.env['crm.lead'].sudo().browse(int(lead_id))
        
        admin_user = request.env['res.users'].sudo().browse(2)
        user_tz = admin_user.tz
            
        local_tz = pytz.timezone(user_tz)
        meeting_start_str = post.get('meeting_start')
        meeting_end_str = post.get('meeting_end')
        
        meeting_start =  datetime.fromisoformat(meeting_start_str)
        meeting_end = datetime.fromisoformat(meeting_end_str)

        if meeting_start and meeting_end:
            try:
                if meeting_start.tzinfo is None:
                    meeting_start = local_tz.localize(meeting_start)

                meeting_start = meeting_start.astimezone(pytz.utc)
                meeting_start = meeting_start.replace(tzinfo=None)
                
                if meeting_end.tzinfo is None:
                    meeting_end = local_tz.localize(meeting_end)

                meeting_end = meeting_end.astimezone(pytz.utc)
                meeting_end = meeting_end.replace(tzinfo=None)

                # Create the calendar event
                request.env['calendar.event'].sudo().create({
                    'name': 'Discussion for {}'.format(lead_id.name),
                    'start': meeting_start,
                    'stop': meeting_end,
                    'show_as': 'free',
                    'privacy': 'confidential',
                    'description': 'Scheduled meeting through website form.',
                    'partner_ids': [(4, partner.id) for partner in lead_id.user_id.partner_id],
                    'opportunity_id': lead_id.id,
                })
            except Exception as e:
                return request.redirect('/contactus-salesenquiry/thank-you')

        return request.redirect('/contactus-salesenquiry/thank-you')
