from odoo import models, fields


class SchoolTeacher(models.Model):
    _name = 'school.teacher'
    _description = 'This is a teacher model'

    name = fields.Char()

    gender = fields.Selection(selection=[
        ('m', 'Male'),
        ('f', 'Female'),
    ])

    school_id = fields.Many2one('school.main')

    classes_ids = fields.Many2many(comodel_name='school.class',
                                   relation='teacher_class_rel',
                                   column1='teacher_id',
                                   column2='class_id',
                                   domain="['|', '|', ('school_id', '=', school_id), ('students_no','<', 10), ('teachers_ids','=',False)]")
