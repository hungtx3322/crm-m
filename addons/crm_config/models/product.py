# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, tools


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @tools.ormcache()
    def _get_default_uom_ids(self):
        uom_ids = self.env['uom.uom'].sudo().search([('id', '!=', self.uom_id.id)])
        return uom_ids.ids

    x_moq = fields.Many2one('product.moq', 'Quy cách đóng gói')
    uom_ids = fields.Many2many('uom.uom', default=_get_default_uom_ids,)





class ProductMoq(models.Model):
    _name = 'product.moq'

    name = fields.Char('Quy cách đóng gói')
