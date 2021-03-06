# -*- coding: utf-8 -*-
from openerp import fields, models, api


class account_invoice_line(models.Model):
    _inherit = 'account.invoice.line'

    @api.one
    # Dummy depend on name so that it is updated on view load
    @api.depends('name')
    def _get_user_restrict_prices(self):
        self.user_restrict_prices = self.env['res.users'].has_group(
            'price_security.group_restrict_prices')

    user_restrict_prices = fields.Boolean(
        compute='_get_user_restrict_prices',
        string='User Restrict Prices')
    product_can_modify_prices = fields.Boolean(
        related='product_id.can_modify_prices',
        readonly=True,
        string='Product Can modify prices')

    @api.one
    @api.constrains(
        'discount', 'user_restrict_prices', 'product_can_modify_prices')
    def check_discount(self):
        if self.user_restrict_prices and not self.product_can_modify_prices and self.invoice_id:
            self.env.user.check_discount(
                self.discount,
                self.invoice_id.partner_id.property_product_pricelist.id)
