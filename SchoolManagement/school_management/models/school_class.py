from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class SchoolClass(models.Model):
    _name = 'school.class'
    _description = 'This is a school class model'

    # _sql_constraints = [
    #     ('students_no_positive', 'check (students_no > 0)', 'The value must be positive'),
    # ]

    name = fields.Char(required=True)

    students_no = fields.Integer()

    school_id = fields.Many2one(comodel_name='school.main', ondelete='cascade')

    @api.onchange('school_id')
    def onchange_school_id(self):
        pass
        # self.students_no = 0

        # unlink all teachers
        # self.teachers_ids = [fields.Command.clear()]
        # self.teachers_ids = [(5, 0, 0)]

        # unlink all teachers except one
        # for rec_id in self.teachers_ids.ids[1:]:
        # self.teachers_ids = [fields.Command.unlink(rec_id)]
        # self.teachers_ids = [(3, rec_id)]

        # delete all all teachers except one
        # for rec_id in self.teachers_ids.ids[1:]:
        #     self.teachers_ids = [fields.Command.delete(rec_id)]

    # def write(self, vals):
    #     raise exceptions.UserError('You are not allowed to change this record')
    #     return super().write(vals)

    # def unlink_teachers(self):
    #     for rec_id in self.teachers_ids.ids:
    #         self.teachers_ids = [fields.Command.unlink(rec_id)]
    #

    def write(self, vals):
        # ex: vals = {'name': 'class2', students_no: 5}
        # if 'name' in vals:
        # if vals['name']:

        if vals.get('name', 'empty') != 'empty':
            raise UserError('You are not allowed to change the class name')
        print(self.name)
        res = super().write(vals)
        print(self.name)

        if vals.get('name', 'empty') != 'empty':

            raise UserError('You are not allowed to change the class name')

        return res
        return super().write(vals)
        res = True
        for record in self:

            # vals['students_no'] = int(record.students_no) + 1

            if vals.get('school_id'):
                teachers_ids_commands = []
                for t in self.teachers_ids:
                    teachers_ids_commands.append(fields.Command.unlink(t.id))
                vals['teachers_ids'] = teachers_ids_commands

                vals['teachers_ids'] = [fields.Command.delete(t.id) for t in self.teachers_ids]

            res = super().write(vals)

            if not record.name.startswith('Class'):
                raise UserError('Class must start with (Class)')

        return res

    # @api.model
    # def search(self):

    @api.model
    def create(self, vals):
        res = super().create(vals)

        if not res.name.startswith('Class'):
            raise UserError('Class must start with (Class)')

        return res

    def unlink(self):
        for record in self:
            if record.students_no > 0:
                raise UserError('Class is not empty')
        return super().unlink()

    # @api.ondelete(at_uninstall=True)
    # def test(self):
    #     print('zzzzzzzzzzzzzzzzz')

    # create, unlink

    # unique_name && student number not < 0
    @api.constrains('name', 'students_no')
    def check_name_student_no(self):
        print('zzzzzzzzzzzzzz')
        # get all names of other records
        # check if = current rec name
        for record in self:
            for class_rec in self.search([('id', '!=', record.id)]):
                if record.name == class_rec.name:
                    raise ValidationError('Class Name must be unique')

            print(record)
            print(record.students_no)

            if record.students_no < 0:
                raise ValidationError('Student Number must be positive')

    teachers_ids = fields.Many2many(comodel_name='school.teacher', relation='teacher_class_rel', column2='teacher_id',
                                    column1='class_id')

    students_ids = fields.One2many('school.student', 'class_id')
