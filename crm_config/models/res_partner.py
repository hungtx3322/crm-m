from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools import format_amount


class ResPartner(models.Model):
    _inherit = 'res.partner'

    x_so_line = fields.One2many('sale.order.line', 'x_partner_id', 'Lịch sử đặt hàng', readonly=True)

    # def _search(self, domain, *args, **kwargs):
    #     if not self.env.is_system() and not self._context.get('show_all_partners'):
    #         user_filter = ['|',  ('user_ids', '=', False),
    #                        ('id', '=', self.env.user.partner_id.id)]
    #         domain = list(domain) + user_filter
    #
    #     return super()._search(domain, *args, **kwargs)
