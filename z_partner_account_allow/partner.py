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


class res_partner(osv.osv):
    _name = 'res.partner'
    _inherit = 'res.partner'
    _description = 'Partner'

    _columns = {
                'property_account_payable': fields.property(
            type='many2one',
            relation='account.account',
            string="Account Payable",
            domain="[('type', '=', ('payable', 'receivable' ))]",
            help="This account will be used instead of the default one as the payable account for the current partner",
            required=True),
        'property_account_receivable': fields.property(
            type='many2one',
            relation='account.account',
            string="Account Receivable",
            domain="[('type', '=', ('payable', 'receivable' ))]",
            help="This account will be used instead of the default one as the receivable account for the current partner",
            required=True),
    }
