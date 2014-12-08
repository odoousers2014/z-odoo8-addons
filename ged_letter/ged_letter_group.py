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
from openerp import api


class ged_discussion_letter(osv.Model):

    _name = 'ged.discussion.letter'
    _description = 'GED Discussion Letter Group'

    _order = "id desc"

    @api.model
    def create(self, vals):
        if ('name' not in vals) or (vals.get('name') == '/'):

            seq_obj_name = self._name
            vals['name'] = self.env['ir.sequence'].get(seq_obj_name)

        new_id = super(ged_discussion_letter, self).create(vals)
        return new_id

    _columns = {
        'name': fields.char(string='Reference', size=64, required=False, readonly=True,),
        'date': fields.date(string='Date letter', readonly=True, help="date discussion started"),

    }


class ged_letter(osv.Model):

    _inherit = 'ged.letter'

    def _get_letter_count(self, cr, uid, ids, field_name, arg, context=None):
        res = dict(map(lambda x: (x, 0), ids))

        try:
            for let in self.browse(cr, uid, ids, context):
                res[let.id] = len(let.letter_ids)
        except:
            pass
        return res

    def _get_letter_ids(self, cr, uid, ids, name, args, context=None):
        res = {}
        for let in self.browse(cr, uid, ids, context=context):
            if let.discussion_id:
                res[let.id] = self.pool.get('ged.letter').search(
                    cr, uid, [('discussion_id', '=', let.discussion_id.id)], context=context)
        return res

    _columns = {
        'discussion_id': fields.many2one('ged.discussion.letter', string='Discussion'),
        'letter_ids': fields.function(_get_letter_ids, method=True, type='one2many', relation='ged.letter', string='Letter associated to same discussion'),
        'letter_count': fields.function(_get_letter_count, string='# of Letters Discussion', type='integer'),
    }
