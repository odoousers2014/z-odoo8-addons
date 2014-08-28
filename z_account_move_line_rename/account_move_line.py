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
from openerp.osv import osv, fields
from openerp.tools.translate import _


class account_move_line(osv.osv):
    _inherit = "account.move.line"

    def write(self, cr, uid, ids, vals, context=None, check=True, update_check=True):
        account_obj = self.pool.get('account.account')
        move_obj = self.pool.get('account.move')
        cur_obj = self.pool.get('res.currency')
        journal_obj = self.pool.get('account.journal')
        if isinstance(ids, (int, long)):
            ids = [ids]

        for line in self.browse(cr, uid, ids, context=context):
            account = line.account_id.name

        org_name = vals['name']
        shortkey = '/**'
        if shortkey in org_name:
            up = account
            vals.update({'name': up})

        result = super(account_move_line, self).write(
            cr, uid, ids, vals, context, check, update_check=False)
        return result

    def create(self, cr, uid, vals, context=None, check=True):

        account_obj = self.pool.get('account.account')
        tax_obj = self.pool.get('account.tax')
        move_obj = self.pool.get('account.move')
        cur_obj = self.pool.get('res.currency')
        journal_obj = self.pool.get('account.journal')

        context = dict(context or {})

        if ('account_id' in vals):
            account = account_obj.browse(
                cr, uid, vals['account_id'], context=context)


        org_name = vals['name']
        shortkey = '/**'

        if shortkey in org_name:
            up = account.name
            vals.update({'name': up})

        result = super(account_move_line, self).create(
            cr, uid, vals, context=context)
        return result


account_move_line()
