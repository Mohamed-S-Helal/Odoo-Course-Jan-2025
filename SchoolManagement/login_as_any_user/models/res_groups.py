# -*- coding: utf-8 -*-
###############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2024-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Sabeel B (odoo@cybrosys.com)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
from base64 import b64encode
from odoo import models, fields, api
from odoo.tools import html_escape, file_open
from hashlib import sha512


def get_hsl_from_seed(seed):
    hashed_seed = sha512(seed.encode()).hexdigest()
    # full range of colors, in degree
    hue = int(hashed_seed[0:2], 16) * 360 / 255
    # colorful result but not too flashy, in percent
    sat = int(hashed_seed[2:4], 16) * ((70 - 40) / 255) + 40
    # not too bright and not too dark, in percent
    lig = 45
    return f'hsl({hue:.0f}, {sat:.0f}%, {lig:.0f}%)'


class ResGroups(models.Model):
    """class to inherit a new field to res groups"""
    _inherit = 'res.groups'

    user_id = fields.Many2one('user.selection', string="User",
                              help="Select User")


class AvatarMixin(models.AbstractModel):
    _inherit = 'avatar.mixin'

    def _avatar_generate_svg(self):
        initial = html_escape(self[self._avatar_name_field].split(' ')[0].upper())
        bgcolor = get_hsl_from_seed(self[self._avatar_name_field] + str(self.create_date.timestamp() if self.create_date else ""))
        return b64encode((
            "<?xml version='1.0' encoding='UTF-8' ?>"
            "<svg height='180' width='180' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'>"
            f"<rect fill='{bgcolor}' height='180' width='180'/>"
            f"<text fill='#ffffff' font-size='96' text-anchor='middle' x='90' y='125' font-family='sans-serif'>{initial}</text>"
            "</svg>"
        ).encode())
