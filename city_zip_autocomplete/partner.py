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
    _inherit = "res.partner"

    zip_id = fields.Many2one('city.zip.autocomplete', string='City/Location')
    departement_id = fields.Many2one('cza.departement', string='Departement',)

    @api.onchange('zip_id')
    def onchange_zip_id(self):
        cza = self.zip_id

        self.zip = cza.name
        self.city = cza.city
        self.departement_id = cza.departement_id.id if cza.departement_id else False
        self.country_id = cza.country_id.id if cza.country_id else False
        self.state_id = cza.state_id.id if cza.state_id else False
