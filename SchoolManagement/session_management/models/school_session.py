# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SchoolSession(models.Model):
    _name = 'school.session'
    _description = 'Session Management'

    def _get_default_code(self):
        all_codes = self.search([]).mapped('name')
        return max(all_codes) + 1 if all_codes else 1

    name = fields.Char(string="Code", required=True, default=_get_default_code)
    school_id = fields.Many2one('school.main')
    class_id = fields.Many2one('school.class', domain=[('school_id', '=', school_id)])
    teacher_id = fields.Many2one('school.teacher', domain=[('classes_ids', 'in', [class_id])])
    students_ids = fields.Many2many('school.student', relation='session_student_rel',domain=[('class_id', '=', class_id)])
    attended_students = fields.Many2many('school.student', relation='session_student_attended_rel',domain=[('class_id', '=', class_id)])
    absent_students_ids = fields.Many2many('school.student', compute='_compute_absent_students_ids', store=False)

    def _compute_absent_students_ids(self):
        for session in self:
            recs = session.students_ids - session.attended_students
            session.absent_students_ids = [(6, 0, recs.ids)]

    content = fields.Html()
    date = fields.Date()
    start_time = fields.Float()
    end_time = fields.Float()
    duration = fields.Float(compute='_compute_duration')

    def _compute_duration(self):
        for session in self:
            session.duration = session.end_time - session.start_time

    status = fields.Selection(selection=[
        ('p', 'Preparation'),
        ('r', 'Running'),
        ('d', 'Done'),
        ('c', 'Cancelled')
    ], default='p')

    @api.constrains('name')
    def unique_name(self):
        for session in self:
            other_sessions = self.search([('id', '!=', session.id)])
            if session.name in other_sessions.mapped('name'):
                raise ValidationError('Session Code must be unique')

    @api.constrains('date', 'start_time', 'end_time', 'teacher_id', 'class_id')
    def check_teacher_overlapping_sessions(self):
        pass
        # validate teacher not have more than one session in the same time and same day
        # validate class not have more than one session in the same time and same day

    @api.onchange('start_time', 'end_time')
    def onchange_time(self):
        if self.start_time and self.end_time and not self.end_time > self.start_time:
            raise ValidationError('Session End time must be > Start time')



