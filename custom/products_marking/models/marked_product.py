from odoo import fields, models, api

PRODUCT_MOVEMENT_STATUS = [
    ("purchase", "Purchase"),
    ("sale", "Sale"),
    ("internal_movement", "Internal movement"),
]


class MarkedProduct(models.Model):
    _name = 'products_marking.marked_product'
    _description = 'Marked Product'

    product_id = fields.Many2one(
        'products_marking.product',
        string="Product",
        required=True, index=True)
    last_assigned_warehouse_id = fields.Many2one(
        'products_marking.warehouse',
        string='Last assigned warehouse',
        required=True)
    last_assigned_status = fields.Selection(
        selection=PRODUCT_MOVEMENT_STATUS,
        string="Last product movement status",
        required=True)
    cost_or_income_item_ids = fields.Many2many(
        'cost_or_income_item',
        string='Cost or income items applied to the marked product',
        required=True
    )
    total_cost = fields.Float(
        string='Total cost',
        compute='_compute_total_cost',
        store=True)
    total_income = fields.Integer(
        string='Total income',
        compute='_compute_total_income',
        store=True)
    total_profit = fields.Integer(
        string='Total profit',
        compute='_compute_total_profit',
        store=True)

    @api.depends('cost_or_income_item_ids.value')
    def _compute_total_cost(self):
        for record in self:
            record.total_cost = sum(
                i.value for i in self.cost_or_income_item_ids if i.cost_or_income_type in [
                    'agent_commission', 'promotion_costs', 'logistics_costs', 'purchase_costs'])

    @api.depends('cost_or_income_item_ids.value')
    def _compute_total_income(self):
        for record in self:
            record.total_income = sum(i.value for i in self.cost_or_income_item_ids if i.cost_or_income_type in [
                'sale_revenue', ])

    @api.depends('total_cost', 'total_income')
    def _compute_total_profit(self):
        for record in self:
            record.total_profit = record.total_income - record.total_cost
