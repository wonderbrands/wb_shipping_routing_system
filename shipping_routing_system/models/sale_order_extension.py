from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Campos generales para todos los paquetes
    zip_code_shipper = fields.Char(string="C.P Origen", readonly=True, copy=False)
    zip_code_recipient = fields.Char(string="C.P Destino", readonly=True, copy=False)
    wb_srs_flag = fields.Boolean(string='¿Procesado por SRS?',default=False, readonly=True, copy=False) #

    # Relación One2many con el nuevo modelo para productos y dimensiones
    routing_lines_ids = fields.One2many(
        comodel_name='sale.order.routing.line',
        inverse_name='sale_order_id',
        string='Lista'
    )

    # Relación One2many con las opciones de paqueterías
    wb_shipping_options = fields.One2many(
        comodel_name='sale.order.shipping.option',
        inverse_name='sale_order_id',
        string='Opciones de Paqueterías'
    )


class SaleOrderRoutingLine(models.Model):
    _name = 'sale.order.routing.line'
    _description = 'Líneas de Enrutamiento'

    # Relación con la orden de venta
    sale_order_id = fields.Many2one(
        comodel_name='sale.order',
        string='Orden de Venta',
        ondelete='cascade'
    )

    # Campos específicos para productos y dimensiones
    product_name_srs = fields.Char(string='Producto', readonly=True)
    packing_length = fields.Float(string="Largo [cm]", readonly=True)
    packing_width = fields.Float(string="Ancho [cm]", readonly=True)
    packing_height = fields.Float(string="Alto [cm]", readonly=True)
    packing_weight = fields.Float(string="Peso [kg]", readonly=True)
    quantity = fields.Integer(string="Unidades", readonly=True)

    # Relación One2many para opciones de envío específicas de esta línea
    shipping_options_ids = fields.One2many(
        comodel_name='sale.order.shipping.option',
        inverse_name='routing_line_id',
        string='Opciones de Envío'
    )

    # Método para abrir el popup de opciones de envío
    def action_open_shipping_options(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Opciones de Envío',
            'res_model': 'sale.order.shipping.option',
            'view_mode': 'tree,form',
            'domain': [('routing_line_id', '=', self.id)],  # Filtrar opciones relacionadas con la línea
            'context': {
                'default_routing_line_id': self.id,  # Predefinir la línea en nuevas opciones
            },
            'target': 'new',  # Abrir como popup modal
        }


class SaleOrderShippingOption(models.Model):
    _name = 'sale.order.shipping.option'
    _description = 'Opciones de Envío'

    # Relación con la orden de venta
    sale_order_id = fields.Many2one(
        comodel_name='sale.order',
        string='Orden de Venta',
        ondelete='cascade'
    )

    # Relación con las líneas de enrutamiento
    routing_line_id = fields.Many2one(
        comodel_name='sale.order.routing.line',
        string='Línea de Enrutamiento',
        ondelete='cascade'
    )

    # Campos para las opciones de envío
    index = fields.Integer(string='Índice', required=True, readonly=True)
    carrier = fields.Text(string='Paquetería', required=True, readonly=True)
    service_type = fields.Char(string='Tipo', required=True, readonly=True)
    price = fields.Monetary(string='Precio', currency_field="currency_id", required=True, readonly=True)
    currency_id = fields.Many2one('res.currency', string="Currency")
    platform = fields.Char(string='Plataforma', required=True, readonly=True)
