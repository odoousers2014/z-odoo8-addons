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
    "name": "City Zip Autocomplete",
    "version": "1.1",
    "depends": ['base',
                'contacts',
                ],
    "author": "Zuher ELMAS",
    "description": """
Complete module for managing addresses.
====================
    - Auto completition address
    - Field Department
    - Relational fields -> Country > State > Departments > City Zip

Integrate databases for all countries with include city and zip
------------------------
Example extension "city_zip_autocomplete_fr"

    - Included more than 37000 cities with postal code

Possibility to create new extension with database for all country
------------------------
    - File of state
    - File of departement (optional)
    - File of cities with zip

See exemple "city_zip_autocomplete_fr"

    """,
    "data": [
          'city_zip_autocomplete.xml',
          'state_view.xml',
          'partner_view.xml',
          'security/ir.model.access.csv',
          ],
    'installable': True,
    'active': False,
#    'certificate': 'certificate',
}