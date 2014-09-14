# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014-Zuher ELMAS.
#
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import itertools
import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from operator import itemgetter
import time

import openerp
from openerp import SUPERUSER_ID, api
from openerp import tools
from openerp.osv import fields, osv, expression
from openerp.tools.translate import _
from openerp.tools.float_utils import float_round as round

import openerp.addons.decimal_precision as dp

_logger = logging.getLogger(__name__)

class account_invoice(osv.osv):

    _inherit = 'account.invoice'


    def inv_line_characteristic_hashcode(self, invoice_line):
        """Overridable hashcode generation for invoice lines. Lines having the same hashcode
        will be grouped together if the journal has the 'group line' option. Of course a module
        can add fields to invoice lines that would need to be tested too before merging lines
        or not."""

        value = "%s-%s-%s-%s"%(
            invoice_line['account_id'],
            invoice_line.get('tax_code_id',"False"),
            invoice_line.get('analytic_account_id',"False"),
            invoice_line.get('date_maturity',"False")
            )
        return value

        return super(account_invoice, self).inv_line_characteristic_hashcode(invoice_line)


    def action_number(self, cr, uid, ids, *args):
        result = super(account_invoice, self).action_number(cr, uid, ids, *args)

        for inv in self.browse(cr, uid, ids):
            if inv.type in ('in_invoice', 'in_refund'):
                if not inv.reference:
                    # ref = self._convert_ref(inv.number)
                    ref = inv.number
                else:
                    ref = inv.reference
            else:
                ref = inv.number

            # invtype = inv.type
            # number = inv.number
            # move_id = inv.move_id and inv.move_id.id or False
            # reference = inv.reference or ''

            partner = '%s' %(inv.move_id.partner_id.name)
            name = '%s' %(inv.number)
            period ='%s' %(inv.move_id.period_id.name)

            custom = '%s %s %s' %(name, period, partner)

            cr.execute('UPDATE account_move SET name=%s ' \
                    'WHERE account_move.name=%s',
                    (inv.move_id.id, custom))

            cr.execute('UPDATE account_move_line SET name=%s ' \
                    'WHERE move_id=%s',
                    (custom, inv.move_id.id))
        return result

account_invoice()

