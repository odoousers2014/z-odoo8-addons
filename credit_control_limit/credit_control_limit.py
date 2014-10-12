# -*- encoding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2013-2014 Zuher ELMAS. All Rights Reserved
#
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from openerp import models, fields, api, _
from openerp.osv import osv

class res_partner(models.Model):

    _inherit = 'res.partner'

    order_policy = fields.Selection([
        ('manual', 'On Demand'),
        ('picking', 'On Delivery Order'),
        ('prepaid', 'Before Delivery'),
    ], 'Invoice method', required=True, default=lambda self: self._context.get('order_policy', 'prepaid'),
        help="""On demand: A draft invoice can be created from the sales order when needed. \nOn delivery order: A draft invoice can be created from the delivery order when the products have been delivered. \nBefore delivery: A draft invoice is created from the sales order and must be paid before the products can be delivered.""")
    amount_not_invoiced = fields.Float(
        string='Not invoiced', readonly=True, compute='_not_invoiced', store=False, help="""Total sale orders confirmed and not invoiced""")
    credit_allow = fields.Boolean(string='Allow Credit', default=False, help=""" Allow credit sales in the authorized limit. If this box is checked, each selling a check will be made of the total amount due by the partner. If the amount due exceeds the allowed limit, the document status to "bloqued". A manager can confirm the order forcing the state.""")

    @api.one
    def _not_invoiced(self):
        sale_obj = self.pool['sale.order']
        self.amount_not_invoiced = 0
        for record in self:
            domain = [('partner_id', '=', record.id), ('state', 'in', ('progress',
                                                                       'manual')), ('shipped', '=', False), ('order_policy', '=', 'picking')]
            sales = sale_obj.search(self._cr, self._uid, domain)
            saleorder = sale_obj.browse(self._cr, self._uid, sales)

            total = 0
            for so_ids in saleorder:
                if so_ids and so_ids[0]:
                    so = so_ids[0]

                total += so.amount_total

                if (so.shipped != True) and (so.picking_ids):
                    invoiced = {}
                    invoiced = sum([x.amount_total for x in so.invoice_ids if x.state in (
                        'open', 'paid', 'proforma', 'proforma2')])

                    total -= invoiced

        self.amount_not_invoiced = total

    @api.onchange('credit_allow', 'order_policy')
    def onchange_order_policy(self):
        if self.credit_allow == True:
            self.order_policy = 'picking'
