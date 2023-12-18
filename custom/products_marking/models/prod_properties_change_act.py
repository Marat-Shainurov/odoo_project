from odoo import api, fields, models

PRODUCT_MOVEMENT_STATUS = [
    ("purchase", "Purchase"),
    ("sale", "Sale"),
    ("internal_movement", "Internal movement"),
]


class ProdPropertiesChangeAct(models.Model):
    _name = 'prod_properties_change_act'
    _description = 'Product Properties Change Act'

    product_id = fields.Many2one(
        'products_marking.product',
        string='Product',
        ondelete='restrict')
    marked_product_ids = fields.Many2many(
        'products_marking.marked_product',
        string='Marked products',
        ondelete='restrict')
    quantity = fields.Integer(string='Quantity')
    status = fields.Selection(
        selection=PRODUCT_MOVEMENT_STATUS,
        string="Product movement status",
        required=True,
        default='sale',
        index=True)
    old_warehouse_id = fields.Many2one(
        'products_marking.warehouse',
        string='Old warehouse',
        help='Warehouse FROM which the products are moved',
        ondelete='restrict')
    new_warehouse_id = fields.Many2one(
        'products_marking.warehouse',
        string='New warehouse',
        help='Warehouse TO which the products are moved',
        required=True,
        ondelete='restrict')
    cost_or_income_ids = fields.Many2many(
        'cost_or_income_item',
        string='Cost or income items',
        help='Cost or income items for the product',
        required=False,
        ondelete='restrict')
    act_creation_date = fields.Date(
        string="Act creation date",
        required=True,
        default=fields.Date.today())

    def apply_act(self, *args, **kwargs):
        """
        This method creates or updates the MarkedProduct instances.

        If self.status is 'purchase' the method creates unique MarkedProduct objects self.quantity times.
        All the cost_or_income_items are assigned with evenly divided values.

        If self.status is not 'purchase' the MarkedProduct instances (passes in self.marked_product_ids)
        are searched in the database and being updated.
        All the cost_or_income_items are assigned with evenly divided values.

        After execution the user is redirected to the MarkedProducts list page.
        """
        if self.status == 'purchase':
            cost_or_income_items_set = set()
            cost_or_income_items_set.update(self.env['cost_or_income_item'].create({
                'cost_or_income_type': i.cost_or_income_type,
                'value': i.value / self.quantity,
                'cost_or_income_date': i.cost_or_income_date
            }) for i in self.cost_or_income_ids)

            for _ in range(self.quantity):
                self.env['products_marking.marked_product'].create(
                    {
                        'product_id': self.product_id.id,
                        'last_assigned_warehouse_id': self.new_warehouse_id.id,
                        'last_assigned_status': self.status,
                        'cost_or_income_item_ids': [(4, item.id) for item in cost_or_income_items_set]})
        else:
            cost_or_income_items_set = set()
            cost_or_income_items_set.update(self.env['cost_or_income_item'].create({
                'cost_or_income_type': i.cost_or_income_type,
                'value': i.value / len(self.marked_product_ids),
                'cost_or_income_date': i.cost_or_income_date
            }) for i in self.cost_or_income_ids)

            for product in self.marked_product_ids:
                marked_product = self.env['products_marking.marked_product'].search(
                    [('id', '=', product.id)])

                marked_product.write({
                    'last_assigned_warehouse_id': self.new_warehouse_id.id,
                    'last_assigned_status': self.status,
                    'cost_or_income_item_ids': [(4, item.id) for item in cost_or_income_items_set]})

        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': 'http://localhost:8069/web#action=90&model=products_marking.marked_product&view_type=list&cids=1&menu_id=70'
        }
