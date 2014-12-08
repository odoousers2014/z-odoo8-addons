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
import openerp
from openerp import tools, api
from openerp.osv import osv, fields
from openerp.osv.expression import get_unaccent_wrapper
from openerp.tools.translate import _


class ged_letter_tags(osv.Model):

    _description = 'Letter Tags'
    _name = 'ged.letter.tags'

    def _get_letter_cat_count(self, cr, uid, ids, field, args, context=None):
        res = {}
        for let in self.browse(cr, uid, ids, context=context):
            res[let.id] = len([x.id for x in let.letter_ids])
        return res

    def name_get(self, cr, uid, ids, context=None):
        if isinstance(ids, (list, tuple)) and not len(ids):
            return []
        if isinstance(ids, (long, int)):
            ids = [ids]
        reads = self.read(cr, uid, ids, ['name', 'parent_id'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if record['parent_id']:
                name = record['parent_id'][1] + ' / ' + name
            res.append((record['id'], name))
        return res

    def name_search(self, cr, uid, name, args=None, operator='ilike', context=None, limit=100):
        if not args:
            args = []
        if not context:
            context = {}
        if name:
            # Be sure name_search is symetric to name_get
            name = name.split(' / ')[-1]
            ids = self.search(
                cr, uid, [('name', operator, name)] + args, limit=limit, context=context)
        else:
            ids = self.search(cr, uid, args, limit=limit, context=context)
        return self.name_get(cr, uid, ids, context)

    @api.multi
    def _name_get_fnc(self, field_name, arg):
        return dict(self.name_get())

    _columns = {
        'name': fields.char('Name', required=True, readonly=False),
        'complete_name': fields.function(_name_get_fnc, type="char", string='Name'),
        'abrev': fields.char('Abbreviation', size=5, required=True, readonly=False),
        'parent_id': fields.many2one('ged.letter.tags', 'Category Parent', select=True, ondelete='cascade'),
        'child_id': fields.one2many('ged.letter.tags', 'parent_id', string='Child Categories'),
        'type': fields.selection([('view', 'View'), ('normal', 'Normal')], 'Category Type', help="A category of the view type is a virtual category that can be used as the parent of another category to create a hierarchical structure."),
        'parent_left': fields.integer('Left Parent', select=1),
        'parent_right': fields.integer('Right Parent', select=1),
        'sequence': fields.integer('Sequence', select=True, help="Order of sequence."),
        'letter_ids': fields.many2many('ged.letter', id1='ged_letter_tags_id', id2='ged_letter_id', string='Letters'),
        'letter_count': fields.function(_get_letter_cat_count, string='# of Letters', type='integer', method=True),
    }

    _sql_constraints = [
        ('abrev_unique', 'unique(abrev)', 'THE ABBREVIATION MUST BE UNIQUE !')
    ]

    _defaults = {
        'type': 'normal',
    }
    _parent_name = "parent_id"
    _parent_store = True
    _parent_order = 'sequence, name'
    _order = 'parent_left'

    def _check_recursion(self, cr, uid, ids, context=None):
        level = 100
        while len(ids):
            cr.execute(
                'select distinct parent_id from ged_letter_tags where id IN %s', (tuple(ids),))
            ids = filter(None, map(lambda x: x[0], cr.fetchall()))
            if not level:
                return False
            level -= 1
        return True

    _constraints = [
        (_check_recursion,
         'Error ! You cannot create recursive category.', ['parent_id'])
    ]

    def child_get(self, cr, uid, ids):
        return [ids]
