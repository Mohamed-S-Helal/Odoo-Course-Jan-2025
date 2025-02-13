from odoo import models, fields, api
from dateutil.relativedelta import relativedelta


class SchoolTeacher(models.Model):
    _name = 'school.teacher'
    _description = 'This is a teacher model'

    personal_photo = fields.Image(max_width=50)

    name = fields.Char()

    gender = fields.Selection(selection=[
        ('m', 'Male'),
        ('f', 'Female'),
    ])

    school_id = fields.Many2one('school.main')

    teacher_stage = fields.Selection(related='school_id.stage', readonly=False, store=True)

    birth_date = fields.Date()

    age = fields.Integer(compute='_compute_age', store=True)

    # graduation_year

    # experience_years

    # experience_months

    @api.depends('birth_date')
    def _compute_age(self):
        # self -> recordset

        for record in self:
            if record.birth_date:
                today = fields.Date.today()
                record.age = relativedelta(today, record.birth_date).years
            else:
                record.age = 25

    classes_ids = fields.Many2many(comodel_name='school.class',
                                   relation='teacher_class_rel',
                                   column1='teacher_id',
                                   column2='class_id',
                                   domain="['|', '|', ('school_id', '=', school_id), ('students_no','<', 10), ('teachers_ids','=',False)]")
