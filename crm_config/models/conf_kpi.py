from odoo import fields, models, api


class DeclareKpi(models.Model):
    _name = 'dec.kpi'
    _description = 'Khai báo KPI'

    name = fields.Char()
    user_id = fields.Many2one('res.users', 'Nhân viên', required=True)
    date_start = fields.Date('Ngày bắt đầu', required=True, default=fields.Date.today, )
    date_end = fields.Date('Ngày kết thúc', required=True, default=fields.Date.today, )

    dec_type = fields.Selection(selection=[('oppor', 'Chỉ tiêu ra được deal'),
                                           ('potential', 'Chỉ tiêu tiềm năng'),
                                           ('deal', 'Deal đầu tiên của khách'),
                                           ], string='Loại hình kinh doanh')
    dec_number = fields.Integer('Số khai báo')
    res_number = fields.Integer('Số đạt được', compute='get_data_results',)
    is_complete = fields.Boolean('Hoàn thành', compute='get_data_results', )

    @api.depends('date_start', 'date_end', 'dec_type', 'dec_number')
    def get_data_results(self):
        for rec in self:
            base_domain = [
                ('user_id', '=', rec.user_id.id),
                ('approach_date', '>=', rec.date_start),
                ('approach_date', '<=', rec.date_end),
                ('active', '=', True)
            ]
            num = 0
            crm_obj = self.env['crm.lead'].sudo()
            if rec.dec_type == 'oppor':
                num = crm_obj.search_count(base_domain)
            elif rec.dec_type == 'potential':
                potential_domain = base_domain + [('is_potential', '=', True)]
                num = crm_obj.search_count(potential_domain)
            elif rec.dec_type == 'deal':
                deal_domain = base_domain + [('order_ids.state', '=', 'sale')]
                num = crm_obj.search_count(deal_domain)

            rec.res_number = num
            rec.is_complete = True if rec.res_number == rec.dec_number else False
