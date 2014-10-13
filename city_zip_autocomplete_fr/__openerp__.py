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
    'name': 'French City Zip Database',
    'category': 'Contact',
    'author': 'Zuher ELMAS',
    'depends': ['city_zip_autocomplete'],
    'version': '1.0',
    'description': """
French City And Zip Database
=====================

    - All States
    - All Departements
    - All City with Zip (more 37200)

Additional database for 'city_zip_autocomplete' addons

Villes et Départements Français
=====================

    - Régions Françaises
    - Départements Français avec DOM-TOM
    - Villes et codes postaux (plus de 37200)

Base de donnée additionelle au module 'city_zip_autocomplete'

    """,

    'active': False,
    'data': [
        'data/res.country.state.csv',
        'data/cza.departement.csv',
        'data/city.zip.autocomplete.csv',
    ],
    'installable': True
}