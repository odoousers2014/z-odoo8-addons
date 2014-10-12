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

from openerp import tools, api
from openerp.osv import osv, fields
from openerp import workflow

class sale_order(osv.osv):
    _inherit = 'sale.order'

    _columns = {
        'state': fields.selection([
            ('draft', 'Draft Quotation'),
            ('sent', 'Quotation Sent'),
            ('cancel', 'Cancelled'),
            ('blocked', 'Blocked'),
            ('waiting_date', 'Waiting Schedule'),
            ('progress', 'Sales Order'),
            ('manual', 'Sale to Invoice'),
            ('shipping_except', 'Shipping Exception'),
            ('invoice_except', 'Invoice Exception'),
            ('done', 'Done'),
            ], 'Status', readonly=True, copy=False, help="Gives the status of the quotation or sales order.\
              \nThe exception status is automatically set when a cancel operation occurs \
              in the invoice validation (Invoice Exception) or in the picking list process (Shipping Exception).\nThe 'Waiting Schedule' status is set when the invoice is confirmed\
               but waiting for the scheduler to run on the order date.", select=True),
    }

    def onchange_partner_id(self, cr, uid, ids, part, context=None):
        result = super(sale_order, self).onchange_partner_id(cr, uid, ids, part, context=context)
        if part:
            policy = self.pool.get('res.partner').browse(cr, uid, part, context=context).order_policy

            if policy:
                result['value']['order_policy'] = policy
        return result


    def action_button_confirm(self, cr, uid, ids, context=None):

        for so in self.browse(cr, uid, ids, context=context):

            credit = so.partner_id.credit + so.partner_id.amount_not_invoiced
            total_due = credit + so.amount_total

            if so.partner_id.credit_allow == True:
                if total_due > so.partner_id.credit_limit:
                    so.signal_workflow('blocked')
                    self.write(cr, uid, ids, {'state': 'blocked'})

                if total_due < so.partner_id.credit_limit:
                    so.signal_workflow('order_confirm')
            else:
                 so.signal_workflow('order_confirm')


        return super(sale_order, self).action_button_confirm(cr, uid, ids, context=context)


    def unblock_order(self, cr, uid, ids, context=None):
        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        self.signal_workflow(cr, uid, ids, 'unblock_order')
        self.signal_workflow(cr, uid, ids, 'order_confirm')
        return True

