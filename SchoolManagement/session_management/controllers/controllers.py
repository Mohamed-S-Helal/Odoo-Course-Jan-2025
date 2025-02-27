# -*- coding: utf-8 -*-
# from odoo import http


# class SessionManagement(http.Controller):
#     @http.route('/session_management/session_management', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/session_management/session_management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('session_management.listing', {
#             'root': '/session_management/session_management',
#             'objects': http.request.env['session_management.session_management'].search([]),
#         })

#     @http.route('/session_management/session_management/objects/<model("session_management.session_management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('session_management.object', {
#             'object': obj
#         })

