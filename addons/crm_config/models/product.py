# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    x_moq = fields.Many2one('product.moq', 'Quy cách đóng gói')


class ProductMoq(models.Model):
    _name = 'product.moq'

    name = fields.Char('Quy cách đóng gói')
