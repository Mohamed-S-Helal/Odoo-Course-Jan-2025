from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo import exceptions


class SchoolTeacher(models.Model):
    _name = 'school.teacher'
    _inherit = ['school.teacher', 'mail.activity.mixin']

    currency_id = fields.Many2one('res.currency', default = lambda self: self.env.company.currency_id)

    bank_account = fields.Char()

    basic_salary = fields.Monetary()

    hour_rate = fields.Monetary()

    housing_allowance = fields.Monetary()