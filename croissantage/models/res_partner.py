from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    croissantage_event_ids = fields.One2many('croissantage.event', 'croissanted_id')
