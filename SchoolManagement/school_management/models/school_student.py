from odoo import models, fields, api
from dateutil.relativedelta import relativedelta


class SchoolStudent(models.Model):
    _name = 'school.student'
    _description = 'This is a student model'

    name = fields.Char(required=True)