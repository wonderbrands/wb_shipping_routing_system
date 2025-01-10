from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    wb_srs_flag = fields.Boolean(string='Shipping Routing Flag', default=False, readonly=True)
    wb_shipping_options = fields.One2many(
        comodel_name='sale.order.shipping.option',
        inverse_name='sale_order_id',
        string='Shipping Options'
    )

    @api.model
    def create(self, vals):
        vals['wb_srs_flag'] = False
        return super(SaleOrder, self).create(vals)

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            order.wb_srs_flag = True
        return res


class SaleOrderShippingOption(models.Model):
    _name = 'sale.order.shipping.option'
    _description = 'Shipping Option'

    sale_order_id = fields.Many2one('sale.order', string='Sale Order', required=True, ondelete='cascade')
    index = fields.Integer(string='Index')
    carrier = fields.Char(string='Carrier', required=True)
    price = fields.Float(string='Price', required=True)