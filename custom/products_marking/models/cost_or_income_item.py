from odoo import fields, models

COST_OR_INCOME_TYPE = [
    ("agent_commission", "Agent commission"),
    ("promotion_costs", "Promotion costs"),
    ("logistics_costs", "Logistics costs"),
    ("purchase_costs", "Purchase costs"),
    ("sale_revenue", "Sale revenue")
]


class CostOrIncomeItem(models.Model):
    _name = 'cost_or_income_item'
    _description = 'Cost or income item for a Product'

    marked_product_id = fields.Many2one('products_marking.marked_product', string="Marked product")
    currency_id = fields.Many2one("res.currency", related="marked_product_id.currency_id")
    cost_or_income_type = fields.Selection(
        selection=COST_OR_INCOME_TYPE,
        string="Cost or income type",
        required=True,
        help='Cost or income type is used for setting the cost/income type for marked products.')
    value = fields.Monetary(
        string='Cost or income value',
        required=True)
    cost_or_income_date = fields.Date(
        default=fields.Date.today(),
        string='Date of cost or income receiving')
