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

class cza_departement(models.Model):

    _name = 'cza.departement'


    name = fields.Char(string='Name Departement', required=True)
    code = fields.Char(string='Code Departement', required=True, size=64)
    state_id = fields.Many2one('res.country.state', string='State')
    country_id = fields.Many2one('res.country', string='Country', )



class city_zip_autocomplete(models.Model):

    _name = 'city.zip.autocomplete'


    name = fields.Char('ZIP', required=True)
    city = fields.Char('City', required=True)
    departement_id = fields.Many2one('cza.departement', 'Departement' )
    state_id = fields.Many2one('res.country.state', 'State')
    country_id = fields.Many2one('res.country', 'Country')



    @api.multi
    @api.depends('name', 'city', 'departement_id', 'country_id')
    def name_get(self):
        result = []
        for cza in self:
            if cza.name:
                name = [cza.name, cza.city]
            else:
                name = [cza.city]

            if cza.departement_id:
                name.append(cza.departement_id.name)

            if cza.country_id:
                name.append(cza.country_id.code)

            result.append((cza.id, ' - '.join(name)))
        return result


    @api.onchange('departement_id')
    def onchange_departement_id(self):
        dep = self.departement_id
        if dep:
            self.state_id = dep.state_id.id


    @api.onchange('state_id', 'country_id')
    def onchange_state_id(self):
        st = self.state_id
        if st:
            self.country_id = st.country_id.id


    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):

        args = args or []
        # if context is None:
        #     context = {}

        if name:
            args = [('name', operator, name)] + args
            # args = self.search([('name', 'ilike', name)] + args, limit=limit)
        if not args:
            args = [('city', operator, name)] + args
            # args = self.search([('city', operator, name)] + args, limit=limit)
        addr = self.search(args, limit=limit)
        return addr.name_get()

    # def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
    #     if args is None:
    #         args = []
    #     if context is None:
    #         context = {}
    #     ids = []
    #     if name:
    #         ids = self.search(cr, uid, [('name', 'ilike', name)] + args, limit=limit)
    #     if not ids:
    #         ids = self.search(cr, uid, [('city', operator, name)] + args, limit=limit)
    #     return self.name_get(cr, uid, ids, context=context)

