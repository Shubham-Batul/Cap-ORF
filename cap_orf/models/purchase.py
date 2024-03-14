from odoo import api, fields, models


class PurchaseORF(models.Model):
    _name = 'purchase.orf'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name')
    vendor_id = fields.Many2one(comodel_name='res.partner', string='Vendor')
    vendor_reference = fields.Char(string='Vendor Reference')
    currency_id = fields.Many2one(comodel_name='res.currency', string='Currency')
    po_date = fields.Date(string='PO DATE')
    destination_detail = fields.Selection([('ddc', 'DDC'), ('poe', 'POE'), ('fob', 'FOB')],
                                          string='DESTINATION DETAIL')
    order_line_ids = fields.One2many(comodel_name='order.line', inverse_name='purchase_id',
                                     string='Order Line')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('orf_in_progress', 'ORF InProgress'),
        ('confirm', 'Confirm')], default='draft', string="State")

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('purchase.orf')
        return super(PurchaseORF, self).create(vals)

    def action_progress(self):
        self.state = 'orf_in_progress'

    def action_confirm_purchase(self):
        self.state = 'confirm'
        # self.env['purchase.order'].create({'name': self.name,
        #                                    'partner_id': self.vendor_id.id,
        #                                    'date_approve': self.po_date,
        #                                    'partner_ref': self.vendor_reference,
        #                                    'destination_detail': self.destination_detail,
        #                                    'currency_id': self.currency_id.id,
        #                                    'orf_id': self.id})
        rfq_vals = {
            'name': self.name,
            'partner_id': self.vendor_id.id,
            'date_approve': self.po_date,
            'partner_ref': self.vendor_reference,
            'destination_detail': self.destination_detail,
            'currency_id': self.currency_id.id,
            'orf_id': self.id
        }
        rfq = self.env['purchase.order'].create(rfq_vals)

        for line in self.order_line_ids:
            rfq_line_vals = {
                'order_id': rfq.id,
                'product_id': line.product_id.id,
                'product_qty': line.quantity,
                'product_uom': line.uom_id.id,
                'price_unit': line.unit_price,
            }
            self.env['purchase.order.line'].create(rfq_line_vals)


class PurchaseInherit(models.Model):
    _inherit = 'purchase.order'

    destination_detail = fields.Selection([('ddc', 'DDC'), ('poe', 'POE'), ('fob', 'FOB')],
                                          string='DESTINATION DETAIL')
    orf_id = fields.Many2one(comodel_name='purchase.orf', string='ORF ID')
