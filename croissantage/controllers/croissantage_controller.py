
from odoo import http, Command
from odoo.http import request


class ControllerCroissantage(http.Controller):
    
    @http.route('/croissantage_list', type='http', auth='public', website=True)
    def croissantage_list(self, **kwargs):
        events = request.env['croissantage.event'].search([
            ('state', '!=', 'new')
        ]).grouped('croissanted_id')
        return request.render("croissantage.page_croissantage", {
            "events": events
        })

    @http.route(['/add_croissantage'], type='http', auth="user", methods=['POST'], website=True, csrf=True)
    def add_croissantage_submit(self, **post):
        input_name = post.get('input_name')
        request.env['croissantage.event'].create({
            'name': input_name,
            'croissanter_ids': [Command.link(request.env.user.partner_id.id)]
        })

        return request.redirect('/croissantage_list')
