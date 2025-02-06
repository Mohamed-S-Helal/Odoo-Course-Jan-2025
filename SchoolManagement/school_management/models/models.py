from odoo import models, fields


class School(models.Model):
    _name = 'school.main'
    _description = 'This is a school model'

    name = fields.Char(string='School Name', required=True, index=True)

    location = fields.Char(string='Address Location')

    phone = fields.Char(string='Phone Number', store=True)

    classes_no = fields.Integer(help='Number of classes in the school', default=20, readonly=True)

    success_rate = fields.Float(string='Rate of Success', groups='base.group_system')

    test_store = fields.Float(store=False)









