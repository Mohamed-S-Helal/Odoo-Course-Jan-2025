# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ResCompany(models.Model):
    _inherit = 'res.company'

    rule1 = fields.Char()
    rule2 = fields.Char()
    rule3 = fields.Char()


class GeneralRules(models.TransientModel):
    _name = 'school.rules'

    company_id = fields.Many2one('res.company', default=lambda self: self.env.company, readonly=True)
    rule1 = fields.Char(related='company_id.rule1', readonly=False)
    rule2 = fields.Char(related='company_id.rule2', readonly=False)
    rule3 = fields.Char(related='company_id.rule3', readonly=False)


class CancelReason(models.TransientModel):
    _name = 'cancel.reason'

    reason = fields.Char(required=True)

    # def add_reason(self):
    #     active_model = self.env.context.get('active_model')
    #     active_id = self.env.context.get('active_id')
    #     active_session = self.env[active_model].browse(active_id)
    #     active_session.cancel_reason = self.reason


    # anothe way

    active_session = fields.Many2one('school.session', invisible=True)

    def add_reason(self):
        # teacher
        self.active_session.cancel_reason = self.reason
        self.active_session.status_cancel()




class SessionState(models.Model):
    _name = 'session.state'
    _order = 'sequence'

    name = fields.Char(required=True)
    sequence = fields.Integer()
    fold = fields.Boolean()
    cancel = fields.Boolean()


class SchoolSession(models.Model):
    _name = 'school.session'
    _inherit = ['mail.activity.mixin', 'mail.thread.main.attachment', 'mail.tracking.duration.mixin']
    _description = 'Session Management'
    _track_duration_field = 'state_id'

    def _get_default_code(self):
        # objects -> names
        # ['session_1', 'session_2', 'session_3']
        # map
        # [1, 2, 3]
        # 3 + 1
        # 'session_4'
        all_codes = self.search([]).mapped(lambda session: int(session.name.split('_')[-1]) if session.name else '')
        return f'session_{max(all_codes) + 1}' if all_codes else 'session_1'

    order_handle = fields.Integer()

    cancel_reason = fields.Char()

    name = fields.Char(string="Code", required=True, default=_get_default_code)
    school_id = fields.Many2one('school.main')
    class_id = fields.Many2one('school.class', domain="[('school_id', '=', school_id)]")
    teacher_id = fields.Many2one('school.teacher', domain="[('classes_ids', 'in', [class_id])]")
    students_ids = fields.Many2many('school.student', relation='session_student_rel',
                                    domain="[('class_id', '=', class_id)]")
    attended_students_ids = fields.Many2many('school.student', relation='session_student_attended_rel',
                                             domain="[('class_id', '=', class_id)]")
    absent_students_ids = fields.Many2many('school.student', compute='_compute_absent_students_ids',
                                           store=True, search='_search_absent_students_ids')

    def _search_absent_students_ids(self, operator, value):
        recs = self.search([]).filtered(lambda s: value in s.absent_students_ids.mapped('name'))

        return [('id', 'in', recs.ids)]

    @api.depends('students_ids', 'attended_students_ids')
    def _compute_absent_students_ids(self):
        for session in self:
            recs = session.students_ids - session.attended_students_ids
            session.absent_students_ids = [(6, 0, recs.ids)]

    content = fields.Text(tracking=True)
    date = fields.Date()
    start_time = fields.Float(store=True)
    end_time = fields.Float()
    duration = fields.Float(compute='_compute_duration', search='_search_duration')

    def _compute_duration(self):
        for session in self:
            session.duration = session.end_time - session.start_time

    def _search_duration(self, operator, value):

        # recs = self.search([('duration', '=', value)])

        recs = self.search([]).filtered(lambda s: s.duration == value)

        return [('id', 'in', recs.ids)]

    status = fields.Selection(selection=[
        ('p', 'Preparation'),
        ('r', 'Running'),
        ('d', 'Done'),
        ('c', 'Cancelled')
    ], default='p')

    state_id = fields.Many2one('session.state', tracking=True)
    cancel = fields.Boolean(related='state_id.cancel')

    rating = fields.Selection(selection=[
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '3'),
        ('5', '3'),
    ], default='1')

    kanban_state = fields.Selection([('normal', 'In Progress'), ('done', 'Done'), ('blocked', 'Blocked')],
                                    default='normal', copy=False)

    def status_running(self):
        # self.status = 'r'
        self.state_id = self.env['session.state'].search([('sequence', '=', 2)], limit=1)

    def status_cancel(self):
        # self.status = 'c'
        self.state_id = self.env['session.state'].search([('cancel', '=', True)], limit=1)

        # return action

    def action_cancel(self):
        # manager
        if self.env.user.has_group('school_management.group_school_manager'):
            self.status_cancel()
        elif self.env.user.has_group('school_management.group_school_teacher'):
            return {
                'name': 'Cancel Reason',
                'type': 'ir.actions.act_window',
                'res_model': 'cancel.reason',
                'view_mode': 'form',
                'target': 'new',
                'context':"{'default_active_session': active_id}"
            }

    @api.constrains('name')
    def unique_name(self):
        for session in self:
            # other_sessions = self.search([('id', '!=', session.id)])
            # if session.name in other_sessions.mapped('name'):
            #     raise ValidationError('Session Code must be unique')

            same_name_records = self.search([('id', '!=', session.id), ('name', '=', session.name)])
            if same_name_records:
                raise ValidationError('Session Code must be unique')

    @api.constrains('date', 'start_time', 'end_time', 'teacher_id', 'class_id')
    def check_teacher_overlapping_sessions(self):
        # validate teacher not have more than one session in the same time and same day
        # get all teacher's other sessions on same day
        # apply check ovarlapping
        for record in self:
            teacher_overlapping_sessions = self.search([
                ('id', '!=', record.id),  # Exclude the current record
                ('teacher_id', '=', record.teacher_id.id),
                ('date', '=', record.date),
                ('start_time', '<', record.end_time),
                ('end_time', '>', record.start_time),
            ])

            if teacher_overlapping_sessions:
                raise ValidationError("The selected time range overlaps with another session.")

            # validate class not have more than one session in the same time and same day

            class_overlapping_sessions = self.search([
                ('id', '!=', record.id),  # Exclude the current record
                ('class_id', '=', record.class_id.id),
                ('date', '=', record.date),
                ('start_time', '<', record.end_time),
                ('end_time', '>', record.start_time),
            ])

            if class_overlapping_sessions:
                raise ValidationError("The selected time range overlaps with another session.")

            #####

            # overlapping_sessions = self.search([
            #     ('id', '!=', record.id),  # Exclude the current record
            #     ('date', '=', record.date),
            #     ('start_time', '<', record.end_time),
            #     ('end_time', '>', record.start_time),
            #     '|',
            #     ('teacher_id', '=', record.teacher_id),
            #     ('class_id', '=', record.class_id),
            # ])
            #
            # if overlapping_sessions:
            #     raise ValidationError("The selected time range overlaps with another session.")

    @api.onchange('start_time', 'end_time')
    def onchange_time(self):
        if self.start_time and self.end_time and not self.end_time > self.start_time:
            raise ValidationError('Session End time must be > Start time')
