from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

stage = [
    ('kg', 'Kinder Garden'),
    ('prim', 'Primary'),
    ('prep', 'Preparatory'),
    ('sec', 'Secondary'),
]


class SchoolStudent(models.Model):
    _name = 'school.student'

    _inherits = {'school.contact': 'contact_id'}

    contact_id = fields.Many2one('school.contact')

    name = fields.Char()

    birth_date = fields.Date(tracking=1)

    age = fields.Integer(compute='_compute_age', store=True)

    user_id = fields.Many2one('res.users')

    student_grade_info = fields.Text(compute='_compute_student_grade_info')

    def _compute_student_grade_info(self):
        for student in self:
            student.student_grade_info = '\n'.join(student.exams_ids.mapped(
                lambda e: f'{e.name}: {e.grade}'
            ))

            # '\n'join(['python: 112', 'java: 110', 'english: 80'])

    id_image = fields.Char()

    summary = fields.Text()

    stage = fields.Selection(selection=stage, required=False, default='kg')
    class_id = fields.Many2one('school.class')

    currency_id = fields.Many2one('res.currency')

    fees = fields.Monetary(currency_field='currency_id')

    paid_fees = fields.Boolean()

    stage_name = fields.Char(compute='_compute_stage_name')

    def _compute_stage_name(self):
        stages = dict(stage)
        for rec in self:
            rec.stage_name = stages.get(rec.stage)

    def move_to_prim(self):
        self.stage = 'prim'

    exams_ids = fields.One2many(
        comodel_name='school.exam',
        inverse_name='student_id', )

    success_ratio = fields.Integer(compute='_compute_success_ratio')

    def _compute_success_ratio(self):
        for rec in self:
            # sum grades
            # sum = 0
            # loop exams -> add grade + sum
            # sum full_grades
            sum_grades = 0
            sum_full_grades = 0

            for exam in rec.exams_ids:
                sum_grades += exam.grade
                sum_full_grades += exam.full_grade

            rec.success_ratio = 100 * sum_grades / sum_full_grades if sum_full_grades else 0

            ##########

            # grades = rec.exams_ids.mapped('grade')
            full_grades = rec.exams_ids.mapped('full_grade')
            #
            # rec.success_ratio = sum(grades)/sum(full_grades) if sum(full_grades) else 0

            #######

            # rec.success_ratio = sum(rec.exams_ids.mapped(lambda e: e.grade/e.full_grade if e.full_grade else 0))

            #####

            rec.success_ratio = sum(rec.exams_ids.filtered(lambda e: e.full_grade > 0).mapped(
                lambda e: e.grade / e.full_grade if e.full_grade else 0))
