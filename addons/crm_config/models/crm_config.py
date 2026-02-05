# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class CrmLead(models.Model):
    _inherit = 'crm.lead'


    business_type = fields.Selection(selection=[('service', 'Thương mại'),
                                                ('manufacturing', 'Sản xuất'), ], string='Loại hình kinh doanh')

    manufacturing_industry_id = fields.Many2one('manufacturing.industry', string='Ngành nghề sản xuất')

    lead_code = fields.Char(string='Mã Lead', copy=False, index=True, readonly=True,
                            default=lambda self: self._get_default_lead_code())

    approach_date = fields.Date(string='Ngày tiếp cận', tracking=True, )

    product_id = fields.Many2one('product.product', string='Sản phẩm quan tâm', domain="[('sale_ok', '=', True)]", )

    required_tonnage = fields.Float(string='Nhu cầu (tấn)', tracking=True, digits=(12, 3), )

    sorder_line_ids = fields.One2many('sale.order.line', 'x_lead_id', string='Danh sách bán hàng')
    is_potential = fields.Boolean('Là khách hàng tiềm năng')

    @api.constrains('partner_name', 'phone')
    def _check_duplicate_lead(self):
        for record in self:
            company_name = record.partner_name
            phone = record.phone
            if company_name or phone:
                domain = ['|', ('active', '=', True), ('active', '=', False)]
                or_conditions = []
                if company_name:
                    or_conditions.append(('partner_name', '=', company_name))
                if phone:
                    or_conditions.append(('phone', '=', phone))
                if or_conditions:
                    if len(or_conditions) > 1:
                        domain.insert(0, '|')
                    domain.extend(or_conditions)
                domain.append(('id', '!=', record.id))
                duplicate_leads = self.search(domain, limit=1)

                if duplicate_leads:
                    error_msg = _("A lead already exists with: ")
                    duplicate_info = []

                    if company_name and duplicate_leads.partner_name == company_name:
                        duplicate_info.append(_("Company Name: %s") % company_name)
                    if phone and duplicate_leads.phone == phone:
                        duplicate_info.append(_("Phone: %s") % phone)

                    error_msg += " or ".join(duplicate_info)
                    error_msg += _(" (Lead: %s)") % duplicate_leads.name

                    raise ValidationError(error_msg)

    def unassign_expired_opportunities(self):
        """Cron job chạy hàng ngày để bỏ gán sale person"""
        today = fields.Date.today()
        deadline = today - timedelta(days=30)

        expired_opps = self.search([
            ('type', '=', 'opportunity'),
            ('user_id', '!=', False),
            ('write_date', '<=', fields.Datetime.to_string(
                datetime.combine(deadline, datetime.min.time())
            ))
        ])
        expired_opps.write({'user_id': False})
        return True

    @api.model
    def _get_default_lead_code(self):
        return self.env['ir.sequence'].next_by_code('crm.lead.code') or '/'
