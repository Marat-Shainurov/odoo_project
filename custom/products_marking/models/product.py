from odoo import fields, models


class Product(models.Model):
    _name = 'products_marking.product'
    _description = 'Product model'

    name = fields.Char(string='Product name', required=True)
    description = fields.Text(string='Product description')
