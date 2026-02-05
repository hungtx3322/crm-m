from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleOrderPaymentTerm(models.Model):
    _name = 'sale.order.payment.term'
    _description = 'Sale Order Payment Term'
    _order = 'sequence, id'

    name = fields.Char(
        string='Tên thanh toán',
        compute='_compute_name',
        store=True
    )

    @api.depends('sequence')
    def _compute_name(self):
        for term in self:
            term.name = f'Thanh toán lần {term.sequence}'

    order_id = fields.Many2one('sale.order',
                               string='Đơn hàng', required=True, ondelete='cascade', index=True)

    sequence = fields.Integer(string='Lần thanh toán', required=True, default=1)

    amount = fields.Monetary(string='Số tiền thanh toán', currency_field='currency_id', required=True)

    payment_date = fields.Date(string='Ngày thanh toán dự kiến', required=True)
    amount_pay = fields.Monetary('Số tiền thực nhận')
    note = fields.Char('Ghi chú')

    is_paid = fields.Boolean(string='Đã thanh toán?', default=False)

    currency_id = fields.Many2one('res.currency', string='Tiền tệ', related='order_id.currency_id', readonly=True,
                                  store=True)


    @api.constrains('amount')
    def _check_amount_positive(self):
        for term in self:
            if term.amount < 0:
                raise ValidationError(_('Số tiền thanh toán phải lớn hơn 0!'))

    @api.constrains('payment_date')
    def _check_payment_date(self):
        for term in self:
            if term.payment_date and term.payment_date < fields.Date.today():
                raise ValidationError(_('Ngày thanh toán không được nhỏ hơn ngày hiện tại!'))
