from odoo import api, fields, models

PRODUCT_MOVEMENT_STATUS = [
    ("purchase", "Purchase"),
    ("sale", "Sale"),
    ("internal_movement", "Internal movement"),
]


class ProdPropertiesChangeAct(models.Model):
    _name = 'prod_properties_change_act'
    _description = 'Product Properties Change Act'

    product = fields.Many2one('products_marking.product', string='Product')
    quantity = fields.Integer(string='Quantity')
    status = fields.Selection(
        selection=PRODUCT_MOVEMENT_STATUS,
        string="Product movement status",
        required=True,
        help='Product movement status is used for setting the products movement status.',
        default='purchase',
        index=True
    )
    old_warehouse = fields.Many2one(
        'products_marking.warehouse',
        string='Old warehouse',
        help='Apply for products from warehouse (movement from warehouse)'
    )
    new_warehouse = fields.Many2one(
        'products_marking.warehouse',
        string='New warehouse',
        help='Assign new warehouse (movement to warehouse)'
    )

    cost_or_income = fields.Many2many('cost_or_income_type', string='Cost or income')
    datetime_act = fields.Datetime(
        string="Act Date",
        required=True,
        help="Creation date of the Act",
        default=fields.Datetime.now)
    #
    # @api.onchange('status')
    # def _onchange_status(self):
    #     if self.status == 'purchase':
    #         self.old_warehouse.required = False
    #     else:
    #         self.old_warehouse.required = True

    def create(self, values):
        if 'status' in values and values['status'] == 'purchase':
            values['old_warehouse'] = False
        return super(ProdPropertiesChangeAct, self).create(values)

    def write(self, values):
        if 'status' in values and values['status'] == 'purchase':
            values['old_warehouse'] = False
        return super(ProdPropertiesChangeAct, self).write(values)
