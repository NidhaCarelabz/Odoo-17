# -*- coding: utf-8 -*-
{
    'name': "Web Form Sales Enquiry",

    'summary': "Template Creation for sales enquiry",

    'description': """Template Creation for sales enquiry
    """,

    'author': "CareLabs",

    'category': 'Uncategorized',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base','website','crm','lead_stages', 'lead_form_customization','product'],

    # always loaded
    'data': [
        
        'views/templates.xml',
    ],
    
    'assets': {
        'web.assets_frontend': [
            'web_form_sales_enquiry/static/src/js/website.js',
        ],
    },
}

