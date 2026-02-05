# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class ManufacturingIndustry(models.Model):
    _name = 'manufacturing.industry'
    _description = 'Ngành nghề sản xuất'

    name = fields.Char('Tên', requied=True)