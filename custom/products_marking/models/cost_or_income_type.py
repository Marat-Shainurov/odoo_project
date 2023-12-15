from odoo import fields, models


class CostOrIncomeType(models.Model):
    _name = 'cost_or_income_type'
    _description = 'Cost or income item for a Product'

    cost_or_income_type = fields.Selection(
        selection=[
            ("agent_commission", "Agent commission"),
            ("promotion_costs", "Promotion costs"),
            ("logistics_costs", "Logistics costs"),
            ("purchase_costs", "Purchase costs"),
            ("sale_revenue", "Sale revenue"),
        ],
        string="Cost or income type",
        required=True,
        help='Cost or income type is used for setting the cost/income type for marked products.'
    )
    value = fields.Integer(string='Cost or income value')
