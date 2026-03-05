from odoo import models, fields, tools


class PartnerSummary(models.Model):
    _name = 'partner.summary'
    _description = 'Thông tin liên hệ rút gọn'
    _auto = False

    name = fields.Char('Tên hiển thị', readonly=True)
    user_id = fields.Many2one('res.users', string='Chuyên viên sale', readonly=True)
    country_id = fields.Many2one('res.country', string='Quốc gia', readonly=True)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                SELECT 
                    p.id as id,
                    p.complete_name as name,
                    p.country_id as country_id,
                    p.user_id as user_id
                FROM res_partner p
                WHERE p.active = True
                AND NOT EXISTS (
                    SELECT 1 
                    FROM res_users u 
                    WHERE u.partner_id = p.id
                )
                AND EXISTS (
                    SELECT 1 
                    FROM sale_order s 
                    WHERE s.partner_id = p.id
                )
            )
        """ % self._table)
