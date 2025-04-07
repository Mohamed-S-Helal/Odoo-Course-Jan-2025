from odoo import models, fields


class School(models.Model):
    _name = 'school.main'
    _rec_name = 'name'
    _description = 'This is a school model'

    _log_access = True

    logo = fields.Image()

    name = fields.Char(string='School Name', required=True, index=True, size=None, trim=True)

    location = fields.Text(string='Address Location')

    phone = fields.Char(string='Phone Number', store=True)

    classes_no = fields.Integer(help='Number of classes in the school', default=20, readonly=True)

    success_rate = fields.Float(string='Rate of Success', groups=None, digits=(3, 4))

    stage = fields.Selection(selection=[
        ('kg', 'Kinder Garden'),
        ('prim', 'Primary'),
        ('prep', 'Preparatory'),
        ('sec', 'Secondary'),
    ], required=False, default='kg')

    next_year_start_date = fields.Date()
    school_day_begin_time = fields.Datetime()

    classes_ids = fields.One2many(comodel_name='school.class', inverse_name='school_id', )





