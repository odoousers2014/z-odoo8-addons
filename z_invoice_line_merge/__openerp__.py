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
{
    "name": "Invoice line merge move",
    "version": "1.1",
    "depends": ['base',
                'account',
                ],
    "author": "Zuher ELMAS",
    "category": "account",
    "description": """

This module merges the invoice lines transferred to accounts move by the account criteria


Original version:
=================
* Product 1             Credit
* Product 2             Credit
* Product 3             Credit
* Taxe account          Credit
* Partner account  Debit

This version:
===============
* Products Merge        Credit
* Taxe account          Credit
* Partner account  Debit

This write move.line with "Number , Period, Partner name" format.


    """,
    "data": [],
    'installable': True,
    'active': False,
#    'certificate': 'certificate',
}