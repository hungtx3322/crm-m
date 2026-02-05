# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Crm config',
    'category': '',
    'summary': '',
    'version': '1.0',
    'description': """""",
    'depends': ['base','crm','mail', 'sale', 'sales_team','sale_management'],
    'data': [
        'data/cron_job.xml',
        'data/sq.xml',
        'security/ir.model.access.csv',
        'security/sale_team.xml',
        # "report/sale_order.xml",
        "report/report_taical_quotation.xml",
        "report/report_order_quotation.xml",
        "report/report_usmb_quotation.xml",
        'views/crm_lead.xml',
        'views/mf_industry.xml',
        'views/sale_order.xml',
        'views/res_partner.xml',
        'views/res_user.xml',
        'views/kpi.xml',
        'views/mail_activity.xml',

    ],

    'assets': {

    },
    'author': 'Odoo S.A.',
    'license': 'OEEL-1',
    'application': True,
    'installable': True,
}
