from odoo import models, fields


class SchoolClass(models.Model):
    _name = 'school.class'
    _description = 'This is a school class model'

    name = fields.Char(required=True)
    students_no = fields.Integer()

    school_id = fields.Many2one(comodel_name='school.main', ondelete='cascade')

    teachers_ids = fields.Many2many(comodel_name='school.teacher', relation='teacher_class_rel', column2='teacher_id', column1='class_id')

