
import itertools
import logging
from collections import defaultdict

from odoo import api, fields, models, tools, _, SUPERUSER_ID
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression


class SchoolMixin(models.AbstractModel):
    _name = 'school.mixin'

    school_id = fields.Many2one('school.main')
    is_fees = fields.Boolean()


class ProductTemplate(models.Model):
    _name = "product.template"
    _inherit = ["product.template", 'school.mixin']


class FeesOrder(models.Model):
    _name = "sale.order"
    _inherit = ["sale.order", 'school.mixin']
