from dateutil.relativedelta import relativedelta
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class SchoolContactData(models.AbstractModel):
    _name = 'school.contact.data'

    name = fields.Char(required=True)
    phone = fields.Char()
    national_id = fields.Char()
    email = fields.Char()
    gender = fields.Selection(selection=[
        ('m', 'Male'),
        ('f', 'Female'),
    ])

    school_id = fields.Many2one('school.main')

    birth_date = fields.Date(tracking=1)

    age = fields.Integer(compute='_compute_age', store=True)

    @api.depends('birth_date')
    def _compute_age(self):
        # self -> recordset
        for record in self:
            if record.birth_date:
                today = fields.Date.today()
                record.age = relativedelta(today, record.birth_date).years
            else:
                record.age = 25


class SchoolContact(models.Model):
    _name = 'school.contact'

    name = fields.Char(required=False)
    phone = fields.Char()
    national_id = fields.Char(string='ID No')
    email = fields.Char()
    gender = fields.Selection(selection=[
        ('m', 'Male'),
        ('f', 'Female'),
    ])

    gender2 = fields.Selection(related='gender', selection=[
        ('m', 'Male2'),
        ('f', 'Female2'),
    ], readonly=False)
    school_id = fields.Many2one('school.main')

    birth_date = fields.Date(tracking=1)

    age = fields.Integer(compute='_compute_age', store=True)

    @api.depends('birth_date')
    def _compute_age(self):
        # self -> recordset
        for record in self:
            if record.birth_date:
                today = fields.Date.today()
                record.age = relativedelta(today, record.birth_date).years
            else:
                record.age = 25


