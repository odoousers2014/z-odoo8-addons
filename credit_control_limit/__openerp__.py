# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
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

{
    'name': 'Credit control limit',
    'version': '1',
    "category" : 'Account',
    'complexity': "easy",
    'description': """
Calculating the amount payable by the partner who has not yet been invoiced. It sum the total amount invoiced nor paid and the total amount due to order not invoiced.

- Allow sales in the authorized credit limit.

- Verification of the total amount due by the partner. If the amount due exceeds the allowed limit, the document state write to "bloqued". A manager can confirm the order by forcing the state or cancel the order.

- If allow_credit is not checked, the credit limit not blocked order.

This module override sale workflow. If you want uninstall this addon, you need update after uninstalling sale module.

    """,
    'author': 'Zuher Elmas',
    'depends': ['sale','stock_account'],
    'data': ['credit_control_limit.xml',
            'sale_workflow.xml',
            'sale_view.xml',],
    'demo_xml': [],
    'test': [],
    'installable': True,
    'application': False,
    'auto_install': False,

}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
