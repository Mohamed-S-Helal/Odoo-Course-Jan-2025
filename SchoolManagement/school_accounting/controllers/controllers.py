# -*- coding: utf-8 -*-
# from odoo import http


# class SchoolAccounting(http.Controller):
#     @http.route('/school_accounting/school_accounting', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/school_accounting/school_accounting/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('school_accounting.listing', {
#             'root': '/school_accounting/school_accounting',
#             'objects': http.request.env['school_accounting.school_accounting'].search([]),
#         })

#     @http.route('/school_accounting/school_accounting/objects/<model("school_accounting.school_accounting"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('school_accounting.object', {
#             'object': obj
#         })

