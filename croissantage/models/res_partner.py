from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    croissantage_event_ids = fields.One2many('croissantage.event', 'croissanted_id')

    def create(self, vals):
        partners = super().create(vals)
        for partner in partners:
            self.env['croissantage.event'].create({
                'name': 'Welcome !',
                'croissanted_id': partner.id
            })
        return partners
