from odoo import models, fields

class ServiceField(models.Model):
    _inherit = 'product.template'

    detailed_type = fields.Selection([
        ('consu', 'Consumable'),
        ('service', 'Service'),
        ('standard', 'Standards')],  # Add the new value 'standard'
        string='Product Type', default='consu', required=True,
        help='A storable product is a product for which you manage stock. The Inventory app has to be installed.\n'
             'A consumable product is a product for which stock is not managed.\n'
             'A service is a non-material product you provide.')
    type = fields.Selection(
        [('consu', 'Consumable'),
         ('service', 'Service'),
         ('standard', 'Standards')],
        compute='_compute_type', store=True, readonly=False, precompute=True)
    def _compute_type(self):      
      for record in self:            
               record.type = record.detailed_type
