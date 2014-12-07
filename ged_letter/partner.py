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

from openerp.osv import fields, osv


class res_partner(osv.osv):
    _inherit = 'res.partner'

    def _get_letter_count(self, cr, uid, ids, field_name, arg, context=None):
        Letter = self.pool('ged.letter')

        return {
            partner_id: {
                'letter_count': Letter.search_count(cr, uid, [('partner_id', '=', partner_id)], context=context)
            }
            for partner_id in ids
        }

    _columns = {
        'letter_count': fields.function(_get_letter_count, string='# of Letters', type='integer', multi="ged_letter"),
        # 'letter_ids': fields.one2many('ged_letter','partner_id','Letter')
    }
