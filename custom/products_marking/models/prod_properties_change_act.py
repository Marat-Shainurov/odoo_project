from odoo import api, fields, models

PRODUCT_MOVEMENT_STATUS = [
    ("purchase", "Purchase"),
    ("sale", "Sale"),
    ("internal_movement", "Internal movement"),
]


class ProdPropertiesChangeAct(models.Model):
    _name = 'prod_properties_change_act'
    _description = 'Product Properties Change Act'

    product_id = fields.Many2one('products_marking.product', string='Product', required=True, ondelete='restrict')
    quantity = fields.Integer(string='Quantity', required=True)
    status = fields.Selection(
        selection=PRODUCT_MOVEMENT_STATUS,
        string="Product movement status",
        required=True,
        default='sale',
        index=True)
    old_warehouse_id = fields.Many2one(
        'products_marking.warehouse',
        string='Old warehouse',
        help='Warehouse FROM which the products are moved')
    new_warehouse_id = fields.Many2one(
        'products_marking.warehouse',
        string='New warehouse',
        help='Warehouse TO which the products are moved',
        required=True)
    cost_or_income_ids = fields.Many2many(
        'cost_or_income_item',
        string='Cost or income items',
        help='Cost or income items for the product',
        required=False)
    datetime_act = fields.Date(
        string="Act creation date",
        required=True,
        help="Creation date of the Act",
        default=fields.Date.today())

    def apply_act(self, *args, **kwargs):
        marked_product = self.env['products_marking.marked_product'].search([('product_id', '=', self.product_id.id)])
        if marked_product.id and self.status != 'purchase':
            marked_product.write({
                'last_assigned_warehouse_id': self.new_warehouse_id.id,
                'last_assigned_status': self.status,
                'cost_or_income_item_ids': [(4, cost_or_income_id.id) for cost_or_income_id in self.cost_or_income_ids]
            })
            return marked_product
        else:
            new_marked_product = self.env['products_marking.marked_product'].create({
                'product_id': self.product_id.id,
                'last_assigned_warehouse_id': self.new_warehouse_id.id,
                'last_assigned_status': self.status,
                'cost_or_income_item_ids': [(4, cost_or_income_id.id) for cost_or_income_id in self.cost_or_income_ids]
            })
            return new_marked_product


# todo
#  1. Add the MarkedProduct model + ondelete behavior for all the related models
#  2. And the business logic to MarkedProduct model and the PPC act applying.
#  3. Styles
