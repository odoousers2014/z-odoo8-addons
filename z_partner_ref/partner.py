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

from openerp.osv import osv, fields

GENERATE_REFS = [('none', 'None'),
                 ('empty', 'For partners with empty references'),
                 ('all', 'For all existing partners')]

class z_partner_ref(osv.osv):

    _inherit = 'res.partner'
    _description = "Z Partner Ref"

    _columns = {
        'ref': fields.char('Reference', size=64, select=1, readonly=True),
    }

    _sql_constraints = [
      ('ref_unique', 'unique(ref)', 'THE FIELD REF CORRESPONDING TO PARTNER MUST BE UNIQUE !')
    ]

    def create(self, cr, uid, vals, context=None):

        if not 'ref' in vals:
            if (vals.get('customer') == True) and (vals.get('supplier') == False):
                vals['ref'] = self.pool.get('ir.sequence').get(cr, uid, 'z.partner.ref.customer')

            if (vals.get('customer') == False) and (vals.get('supplier') == True):
                vals['ref'] = self.pool.get('ir.sequence').get(cr, uid, 'z.partner.ref.supplier')

            if (vals.get('supplier') == True) and (vals.get('customer') == True):
                vals['ref'] = self.pool.get('ir.sequence').get(cr, uid, 'z.partner.ref.customer')

            if (vals.get('supplier') == False) and (vals.get('customer') == False):
                vals['ref'] = self.pool.get('ir.sequence').get(cr, uid, 'z.partner.ref.third')


        return super(z_partner_ref, self).create(cr, uid, vals, context=context)

    def copy(self, cr, uid, id, default=None, context=None):
        if default is None:
            default = {}
        default = default.copy()
        partner_obj = self.browse(cr, uid, id, context=context)

        if (partner_obj.customer == True) and (partner_obj.supplier == False):
            default['ref'] = self.pool.get('ir.sequence').get(cr, uid, 'z.partner.ref.customer')
        if (partner_obj.customer == False) and (partner_obj.supplier == True):
            default['ref'] = self.pool.get('ir.sequence').get(cr, uid, 'z.partner.ref.supplier')
        if (partner_obj.customer == True) and (partner_obj.supplier == True):
            default['ref'] = self.pool.get('ir.sequence').get(cr, uid, 'z.partner.ref.customer')
        if (partner_obj.customer == False) and (partner_obj.supplier == False):
            default['ref'] = self.pool.get('ir.sequence').get(cr, uid, 'z.partner.ref.third')

        res = super(z_partner_ref, self).copy(cr, uid, id, default, context)
        return res



z_partner_ref()

class z_partner_ref_config(osv.osv_memory):

    _name = 'z.partner.ref.config'
    _inherit = 'res.config'

    _columns = {
        'generate_ref': fields.selection(GENERATE_REFS, 'Generate Partner references', required=True),
    }

    def execute(self, cr, uid, ids, context=None):
        for config in self.read(cr, uid, ids, ['generate_ref']):
            partner_ids = []
            if config['generate_ref'] == 'all':
                partner_ids += self.pool.get('res.partner').search(cr, uid, [], order='id asc', context=None)
            elif config['generate_ref'] == 'empty':
                partner_ids += self.pool.get('res.partner').search(cr, uid, ['|', ('ref', '=', False), ('ref', '=', '')], order='id asc', context=None)


            for partner_id in partner_ids:
                p_ids = self.pool.get('res.partner')
                p_id = p_ids.browse(cr, uid, partner_id, context=context)
                if (p_id.customer == True) and (p_id.supplier == False):
                    seq_id = 'z.partner.ref.customer'
                if (p_id.customer == False) and (p_id.supplier == True):
                    seq_id = 'z.partner.ref.supplier'
                if (p_id.customer == True) and (p_id.supplier == True):
                    seq_id = 'z.partner.ref.customer'
                if (p_id.customer == False) and (p_id.supplier == False):
                    seq_id = 'z.partner.ref.third'

                self.pool.get('res.partner').\
                    write(cr, uid, partner_id,
                          {'ref': self.pool.get('ir.sequence').get(cr, uid, seq_id)}

                          )

            partner_ids = []
            partner_ids += self.pool.get('res.partner').search(cr, uid, [('ref', '=', False)], context=None)
            partner_ids += self.pool.get('res.partner').search(cr, uid, [('ref', '=', '')], context=None)
            if partner_ids:
                raise osv.except_osv('Error', 'There is empty references !')

            duplicates = cr.execute("""
                SELECT COUNT(ref)
                FROM res_partner
                GROUP BY ref
                HAVING ( COUNT(ref) > 1 )
            """)
            if duplicates:
                raise osv.except_osv('Error', 'There is duplicates references !')

        return True

z_partner_ref_config()

