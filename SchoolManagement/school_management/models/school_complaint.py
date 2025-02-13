from odoo import models, fields


class SchoolComplaint(models.Model):
    _name = 'school.complaint'
    _description = 'This is a school class model'

    name = fields.Char(required=True)

    complaint_subject = fields.Reference(selection=[
        ('school.class', 'Class'),
        ('school.teacher', 'Teacher'),
    ], )

    res_model = fields.Char()

    complainer = fields.Many2oneReference(model_field='res_model')

    complainer_name = fields.Char(compute='_compute_complainer_name')

    def _compute_complainer_name(self):
        for rec in self:
            obj = self.env[self.res_model].browse(self.complainer)
            print(obj)
            rec.complainer_name = obj.name

    # def get_today(self):
    #     today = fields.Date.today()
    #     return today

    date = fields.Date(default=fields.Date.today)

