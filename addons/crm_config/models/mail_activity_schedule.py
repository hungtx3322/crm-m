# -*- coding: utf-8 -*-
# Copyright 2019 Coop IT Easy SCRL fs
#   Robin Keunen <robin@coopiteasy.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class MailActivitySchedule(models.TransientModel):
    _inherit = 'mail.activity.schedule'

    x_time = fields.Float('Giờ')

    def _action_schedule_activities(self):
        res = super()._action_schedule_activities()
        if self.x_time and res:
            res.write({'x_time': self.x_time})
        return res

    def _action_schedule_activities_personal(self):
        res = super()._action_schedule_activities_personal()
        if self.x_time and res:
            res.write({'x_time': self.x_time})
        return res



class MailActivity(models.Model):
    _inherit = 'mail.activity'

    x_time = fields.Float('Giờ')
