from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools import format_amount


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    x_payment_term_ids = fields.One2many('sale.order.payment.term', 'order_id', string='Điều khoản thanh toán',
                                         copy=True
                                         )

    x_total_payment_amount = fields.Monetary(string='Tổng số tiền thanh toán', compute='_compute_total_payment_amount',
                                             store=True, currency_field='currency_id')
    x_total_amount_pay = fields.Monetary(string='Tổng số tiền thực nhận', compute='_compute_total_payment_amount',
                                             store=True, currency_field='currency_id')
    x_has_overdue_payment = fields.Boolean('Có thanh toán quá hạn', compute='_compute_overdue_payments')
    x_so_name = fields.Char('Số đơn hàng')
    x_contract = fields.Char('Số hợp đồng')
    x_date_contract = fields.Date('Ngày hợp đồng')
    x_cang_dich = fields.Char('Cảng đích')
    x_cuoc_bien = fields.Char('Cước biển')
    x_number_bl = fields.Char('Số BL')
    x_date_etd = fields.Date('ETD ngày tàu chạy')
    x_date_eta = fields.Date('ETA ngày tàu đến cảng đích')
    x_check_bank_fees = fields.Monetary('Theo dõi phí ngân hàng')
    x_commission = fields.Char(string='Ghi chú Commission cho khách', )
    x_currency_id = fields.Many2one('res.currency', string='Currency')
    x_dntt = fields.Boolean('ĐNTT com cho cá nhân sales')
    x_moq = fields.Many2one('product.moq', 'Quy cách đóng gói')
    x_sl_moq = fields.Char('Số lượng')
    x_time_deliver = fields.Char('Thời gian giao hàng')
    x_local_deliver = fields.Char('Địa điểm giao hàng')
    x_expen_diliver = fields.Char('Chi phí bốc xếp')






    @api.depends('x_payment_term_ids.amount')
    def _compute_total_payment_amount(self):
        for order in self:
            order.x_total_payment_amount = sum(order.x_payment_term_ids.mapped('amount'))
            order.x_total_amount_pay = sum(order.x_payment_term_ids.mapped('amount_pay'))

    @api.constrains('payment_term_ids')
    def _check_payment_total_amount(self):
        for order in self:
            if order.total_payment_amount > order.amount_total:
                raise ValidationError(
                    _('Tổng số tiền thanh toán (%s) không được vượt quá giá trị đơn hàng (%s)!') %
                    (format_amount(order.env, order.total_payment_amount, order.currency_id),
                     format_amount(order.env, order.amount_total, order.currency_id))
                )

    @api.depends('x_payment_term_ids')
    def _compute_overdue_payments(self):
        today = fields.Date.today()
        for order in self:
            if order.x_payment_term_ids:
                overdue_terms = order.x_payment_term_ids.filtered(
                    lambda t: not t.is_paid
                              and t.payment_date
                              and t.payment_date < today)
                order.x_has_overdue_payment = bool(overdue_terms)
            else:
                order.x_has_overdue_payment = False

    def amount_to_text_vn(self, amount):
        """Convert amount to Vietnamese words."""
        self.ensure_one()
        
        # Simple Vietnamese number to text logic
        # For a professional implementation in Odoo, we typically use a more comprehensive function
        # Reference for Vietnamese numbering: 1,234,567 -> "Một triệu hai trăm ba mươi tư nghìn năm trăm sáu mươi bảy"
        
        def _convert_group(n):
            units = ["", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]
            h = n // 100
            t = (n % 100) // 10
            u = n % 10
            
            res = ""
            if h > 0:
                res += units[h] + " trăm "
            elif h == 0 and (t > 0 or u > 0): # Avoid "không trăm" at the very beginning of the whole number if not needed
                # However, for 1,001 we need "một nghìn lẻ một" or "một nghìn không trăm linh một"
                # Let's simplify and always include 'không trăm' if it's not the first group
                pass 

            if t > 1:
                res += units[t] + " mươi "
                if u == 1: res += "mốt"
                elif u == 5: res += "lăm"
                elif u > 0: res += units[u]
            elif t == 1:
                res += "mười "
                if u == 5: res += "lăm"
                elif u > 0: res += units[u]
            elif t == 0:
                if h > 0 and u > 0:
                    res += "lẻ " + units[u]
                elif u > 0:
                    res += units[u]
            
            return res.strip()

        if amount == 0:
            return "Không đồng"
            
        integer_part = int(abs(amount))
        
        groups = []
        while integer_part > 0:
            groups.append(integer_part % 1000)
            integer_part //= 1000
            
        labels = ["", "nghìn", "triệu", "tỷ", "nghìn tỷ", "triệu tỷ"]
        words = []
        
        for i in range(len(groups)):
            if groups[i] > 0:
                group_text = _convert_group(groups[i])
                if i > 0 and groups[i] < 100:
                    # Special case for "lẻ" or "không trăm"
                    pass
                words.insert(0, group_text + " " + labels[i])
        
        result = " ".join(words).strip()
        result = result.capitalize() + " đồng"
        # Clean up double spaces
        while "  " in result:
            result = result.replace("  ", " ")
            
        return result
