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

import time

from openerp import tools
from openerp.tools.translate import _
from openerp.osv import fields, osv

from openerp import pooler
from openerp import netsvc
from openerp import SUPERUSER_ID


class document_file(osv.osv):

    _inherit = 'ir.attachment'

    _columns = {
        'ged_letter_id': fields.many2one('ged.letter', 'Letter Id', help="If this link for origin object.", select=True),
    }

    def create(self, cr, uid, vals, context=None):

        if context is None:
            context = {}

        vals['ged_letter_id'] = context.get(
            'ged_letter_id', False) or vals.get('ged_letter_id', False)
        # take partner from uid
        if vals.get('res_id', False) and vals.get('res_model', False) and not vals.get('ged_letter_id', False):
            vals['ged_letter_id'] = self.__get_ged_letter_id(
                cr, uid, vals['res_model'], vals['res_id'], context)
        if vals.get('datas', False):
            vals['file_type'], vals['index_content'] = self._index(
                cr, uid, vals['datas'].decode('base64'), vals.get('datas_fname', False), None)
        return super(document_file, self).create(cr, uid, vals, context)

    def __get_ged_letter_id(self, cr, uid, res_model, res_id, context=None):
        """ A helper to retrieve the associated partner from any res_model+id
            It is a hack that will try to discover if the mentioned record is
            clearly associated with a partner record.
        """
        """
        let_receipt = let_receipt_obj.browse(cr, uid, record_id, context=context)
        """

        obj_model = self.pool.get(res_model)
        if obj_model._name == 'ged.letter':
            return res_id

        elif 'ged_letter_id' in obj_model._columns and obj_model._columns['ged_letter_id']._obj == 'ged.letter':
            bro = obj_model.browse(cr, uid, res_id, context=context)
            return bro.ged_letter_id.id
        return False


document_file()
