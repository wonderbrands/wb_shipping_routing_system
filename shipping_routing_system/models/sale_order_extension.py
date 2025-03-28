from odoo import models, fields, api


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
    sku_code = fields.Char(string='SKU')
    product_name_srs = fields.Char(string='Paquete', readonly=True)
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
            'name': f'Opciones de envío para: {self.sku_code} - {self.product_name_srs}',  # 'Opciones de envío',
            'res_model': 'sale.order.shipping.option',
            'view_mode': 'tree,form',
            'domain': [('routing_line_id', '=', self.id)],  # Filtrar opciones relacionadas con la línea
            'context': {
                'default_routing_line_id': self.id,  # Predefinir la línea en nuevas opciones
                'default_name': f'Opciones de envío para: NO PROCESADO'
            },
            'target': 'new',  # Abrir como popup modal
        }

    # Campo del SKY? y nombre concatenados
    product_display_name = fields.Char(
        string='Producto (SKU + Nombre)',
        compute='_compute_product_display_name',
        store=True,
    )

    @api.depends('sku_code', 'product_name_srs')
    def _compute_product_display_name(self):
        for record in self:
            record.product_display_name = f"{record.sku_code or ''} - {record.product_name_srs or ''}"

    # /////////////////////// Nuevo campo para opcion 1 de envio////////////////////////////////////////
    first_shipping_option = fields.Char(
        string="Primera Opción de Envío",
        compute="_compute_first_shipping_option",
        store=True
    )

    @api.depends('shipping_options_ids')
    def _compute_first_shipping_option(self):
        for record in self:
            first_option = record.shipping_options_ids.filtered(lambda opt: opt.index == 1)
            if first_option:
                record.first_shipping_option = f"{first_option[0].carrier} ({first_option[0].platform}): {first_option[0].currency_id.symbol}{first_option[0].total_cost}"
            else:
                record.first_shipping_option = "No hay opción 1"

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
    carrier = fields.Char(string='Paquetería', required=True, readonly=True)
    service_type = fields.Char(string='Tipo', required=True, readonly=True)
    currency_id = fields.Many2one('res.currency', string="Moneda", default=lambda self: self.env.company.currency_id.id)  # 33
    price = fields.Monetary(string='Precio', readonly=True, currency_field='currency_id')
    platform = fields.Char(string='Plataforma', required=True, readonly=True)

    package_quantities = fields.Integer(string="Cantidad", readonly=True)
    strategy = fields.Char(string='Estrategia', required=True, readonly=True)
    smallest_dimension = fields.Char(string='Dimención de agrupación', required=True, readonly=True)
    total_cost = fields.Monetary(string='Precio total', readonly=True, currency_field='currency_id')

    # Campos 18 marzo 2025
    rate_id = fields.Char(string='Rate id', required=True, readonly=True)
    quote_date = fields.Datetime(string='Fecha', required=True, readonly=True)
    status_rate = fields.Char(string='Estado', required=True, readonly=True)
