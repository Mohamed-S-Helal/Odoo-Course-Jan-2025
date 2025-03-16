from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo import exceptions


class SchoolTeacher(models.Model):
    _name = 'school.teacher'
    _inherit = ['mail.thread.main.attachment', 'mail.activity.mixin', 'school.contact']
    _description = 'This is a teacher model'

    user_id = fields.Many2one('res.users')

    company_id = fields.Many2one('res.company')

    def test(self):
        print('Hello')

    number = fields.Integer()

    personal_photo = fields.Image(max_width=50)

    teacher_stage = fields.Selection(related='school_id.stage', readonly=False, store=True)

    @api.onchange('teacher_stage', 'experience_years')
    def onchange_teacher_stage(self):
        # validate teacher yrs of xp >= 5
        print(self.teacher_stage, self.experience_years)
        if self.teacher_stage == 'sec' and self.experience_years < 5:
            raise exceptions.UserError('Teacher Experience must be >= 5')

    graduation_year = fields.Date()

    experience_years = fields.Integer(compute='_compute_experience', inverse='_compute_graduation_year', store=True)

    experience_months = fields.Integer(compute='_compute_experience', inverse='_compute_graduation_year', store=True)

    experience_days = fields.Integer(compute='_compute_experience', inverse='_compute_graduation_year', store=True)

    @api.depends('graduation_year')
    def _compute_experience(self):
        for record in self:
            if record.graduation_year:
                today = fields.Date.today()
                delta = relativedelta(today, record.graduation_year)
                record.experience_years = delta.years
                record.experience_months = delta.months
                record.experience_days = delta.days
            else:
                record.experience_years = 0
                record.experience_months = 0
                record.experience_days = 0

    def _compute_graduation_year(self):
        for record in self:
            today = fields.Date.today()
            delta = relativedelta(years=record.experience_years, months=record.experience_months,
                                  days=record.experience_days)
            record.graduation_year = today - delta

    classes_ids = fields.Many2many(comodel_name='school.class',
                                   relation='teacher_class_rel',
                                   column1='teacher_id',
                                   column2='class_id',)

    def clear_classes(self):
        self.classes_ids = [(5, 0, 0)]
