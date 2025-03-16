from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo import exceptions


class SchoolEmployee(models.Model):
    _name = 'school.employee'
    _inherits = {'school.contact': 'contact_id'}

    contact_id = fields.Many2one('school.contact')

    job_title = fields.Char()
    manager_id = fields.Many2one('school.employee')

    user_id = fields.Many2one('res.users')