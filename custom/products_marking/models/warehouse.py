from odoo import fields, models


class Warehouse(models.Model):
    _name = 'products_marking.warehouse'
    _description = 'Warehouse'

    name = fields.Char(string='Warehouse name', required=True)
    company = fields.Char(string='Warehouse company', required=True)
    city = fields.Char(string='Warehouse city')
    address = fields.Char(string='Warehouse address')
