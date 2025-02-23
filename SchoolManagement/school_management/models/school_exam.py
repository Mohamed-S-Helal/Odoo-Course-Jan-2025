from odoo import models, fields, api


class SchoolExam(models.Model):
    _name = 'school.exam'

    name = fields.Char()

    grade = fields.Integer()
    full_grade = fields.Integer()

    exam_duration = fields.Float()

    student_id = fields.Many2one('school.student')

    sequence = fields.Integer()

    description = fields.Text()

    date_start = fields.Datetime()
    date_end = fields.Datetime()

    exam_scan_paper = fields.Binary(attachment=True)

    exam_scan_answer = fields.Many2many('ir.attachment')

    grade_percent = fields.Float(compute='_compute_grade_percent')

    @api.depends('full_grade', 'grade')
    def _compute_grade_percent(self):
        for rec in self:
            rec.grade_percent = rec.grade/rec.full_grade if rec.full_grade else 0

