# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models

class ResUsers(models.Model):
    _inherit = 'res.users'

    x_name_en = fields.Char('Tên tiếng anh')

