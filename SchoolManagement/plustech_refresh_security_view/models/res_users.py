# -*- coding: utf-8 -*-
#################################################################################
# Author      : Plus Technology Co.Ltd. (<https://www.plustech-it.com//>)
# Copyright(c): 2024-Present Plus Technology Co. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
#################################################################################
from odoo import fields, models


class Users(models.Model):

    _inherit = 'res.users'

    def refresh_view(self):
        self.env["res.groups"].sudo()._update_user_groups_view()
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }