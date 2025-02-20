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
    _description = 'This is a student model'

    name = fields.Char(required=True)

    national_id = fields.Char()
    email = fields.Char()
    phone = fields.Char()
    id_image = fields.Char()

    summary = fields.Text()

    stage = fields.Selection(selection=stage, required=False, default='kg')

    stage_name = fields.Char(compute='_compute_stage_name')

    def _compute_stage_name(self):
        stages = dict(stage)
        for rec in self:
            rec.stage_name = stages.get(rec.stage)

    def move_to_prim(self):
        self.stage = 'prim'
