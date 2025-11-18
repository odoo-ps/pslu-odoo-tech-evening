from odoo import models, fields, api, _
from odoo.exceptions import UserError


class CroissantageEvent(models.Model):
    _name = 'croissantage.event'
    _inherit = 'mail.thread'
    _description = 'Croissantage Event'

    name = fields.Char()
    croissanted_id = fields.Many2one('res.partner')
    city = fields.Char(related='croissanted_id.city')

    croissanter_ids = fields.Many2many('res.partner', string='Croissanters')
    state = fields.Selection([
        ('new', 'Croissanted'),
        ('ongoing', 'Croissants Provided'),
        ('done', 'Debt Paid')
    ], default='new', tracking=True)

    date_start = fields.Date('Date of Croissantage', default=fields.Date.today())
    date_end = fields.Date('Date of Debt Payment')
    duration = fields.Integer('Duration (days)', compute='_compute_duration', store=True)

    def act_validate(self):
        self.ensure_one()
        self.state = 'done'

    @api.depends('date_start', 'date_end')
    def _compute_duration(self):
        for rec in self:
            rec.duration = (rec.date_end - rec.date_start).days if rec.date_end else 0

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for rec in self:
            if rec.date_end and rec.date_end < rec.date_start:
                raise UserError(_('End date must be later than the start date.'))
