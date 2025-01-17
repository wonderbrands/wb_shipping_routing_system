from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Campos calculados para mostrar la información del producto
    product_name = fields.Char(string="Nombre del Producto", compute="_compute_product_info", store=True)
    product_dimensions = fields.Char(string="Dimensiones del Paquete", compute="_compute_product_info", store=True)

    wb_srs_flag = fields.Boolean(string='Shipping Routing Flag', default=False, readonly=True)
    wb_shipping_options = fields.One2many(
        comodel_name='sale.order.shipping.option',
        inverse_name='sale_order_id',
        string='Shipping Options'
    )

    @api.depends('order_line.product_id', 'order_line.product_uom_qty')
    def _compute_product_info(self):
        for order in self:
            if order.order_line:
                # Extraemos los datos del primer producto en las líneas de la orden
                product = order.order_line[0].product_id
                product_length = product.product_length
                product_width = product.product_width
                product_height = product.product_height
                product_weight = product.product_weight
                quantity = order.order_line[0].product_uom_qty

                # Concatenamos las dimensiones y la cantidad
                order.product_name = product.name
                order.product_dimensions = f"Long: {product_length} cm, Width: {product_width} cm, Height: {product_height} cm, Weight: {product_weight} kg, Quantity: {quantity} units"
            else:
                order.product_name = ""
                order.product_dimensions = ""

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