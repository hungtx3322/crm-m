from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools import format_amount


class ResPartner(models.Model):
    _inherit = 'res.partner'

    x_so_line = fields.One2many('sale.order.line', 'x_partner_id', 'Lịch sử đặt hàng', readonly=True)
    source_id = fields.Many2one('utm.source', string='Source', ondelete='restrict', copy=False)
    user_id = fields.Many2one('res.users', default=lambda self: self.env.context.get('user_id', self.env.user.id))

    @api.constrains('partner_name', 'phone')
    def _check_duplicate_lead(self):
        for r in self:
            if r.country_id.code ==  "VN" or r.country_id.name =='Vietnam':
                company_name = r.partner_name
                phone = r.phone
                website = r.website
                if company_name or phone or website:
                    domain = ['|', ('active', '=', True), ('active', '=', False)]
                    or_conditions = []
                    if company_name:
                        or_conditions.append(('partner_name', '=', company_name))
                    if phone:
                        or_conditions.append(('phone', '=', phone))
                    if website:
                        or_conditions.append(('website', '=', website))
                    if or_conditions:
                        if len(or_conditions) > 1:
                            domain.insert(0, '|')
                        domain.extend(or_conditions)
                    domain.append(('id', '!=', r.id))
                    duplicate_leads = self.search(domain, limit=1)
                    if duplicate_leads:
                        error_msg = _("Đã tồn tại lead tương tự: ")
                        duplicate_info = []

                        if company_name and duplicate_leads.partner_name == company_name:
                            duplicate_info.append(_("Company Name: %s") % company_name)
                        if phone and duplicate_leads.phone == phone:
                            duplicate_info.append(_("Phone: %s") % phone)
                        if website and duplicate_leads.website == website:
                            duplicate_info.append(_("website: %s") % website)

                        error_msg += " or ".join(duplicate_info)
                        error_msg += _(" (Lead: %s)") % duplicate_leads.name

                        raise ValidationError(error_msg)

    @api.model_create_multi
    def create(self, vals_list):
        if self.env.context.get('import_file'):
            for values in vals_list:
                if 'user_id' not in values or values.get('user_id') == False:
                    values['user_id'] = self.env.user.id
        return super().create(vals_list)


    def _get_sale_order_domain_count(self):
        domain = super(ResPartner, self)._get_sale_order_domain_count()
        domain.append(('state', '=', 'sale'))
        return domain