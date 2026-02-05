# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    x_lead_id = fields.Many2one('crm.lead', string='Crm lead', related='order_id.opportunity_id', store=True)
    x_name_so = fields.Char('Mã đơn', related='order_id.name', store=True)
    x_partner_id = fields.Many2one('res.partner', related='order_id.partner_id', store=True)
    x_quotation_date = fields.Datetime('Ngày báo giá', related='order_id.date_order', store=True)
    x_description = fields.Text('Mô tả', related='name', readonly=False, store=True)
