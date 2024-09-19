from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    croissantage_ids = fields.One2many('croissantage', 'partner_id')

    def create(self, vals):
        partners = super().create(vals)
        for partner in partners:
            self.env['croissantage'].create({
                'name': 'Welcome !',
                'partner_id': partner.id
            })
        return partners
