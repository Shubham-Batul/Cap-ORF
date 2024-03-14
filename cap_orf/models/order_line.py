from odoo import api, fields, models


class OrderLine(models.Model):
    _name = 'order.line'

    product_id = fields.Many2one(comodel_name='product.product', string='Product')
    image = fields.Binary(string='Image')
    quantity = fields.Float(string='Quantity')
    uom_id = fields.Many2one(comodel_name='uom.uom', string='UOM')
    unit_price = fields.Float(string='Unit price')
    currency_id = fields.Many2one(comodel_name='res.currency', default=lambda self: self.env.company.currency_id)
    subtotal = fields.Monetary(currency_field='currency_id', string='Subtotal')

    purchase_id = fields.Many2one(comodel_name='purchase.orf', string='Purchase')

    @api.onchange('unit_price')
    def onchange_subtotal_price(self):
        if self.unit_price:
            self.subtotal = self.unit_price * self.quantity


