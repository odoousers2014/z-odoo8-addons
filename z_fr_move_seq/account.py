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
                 ('empty', 'For moves with empty references'),
                 ('all', 'For all existing moves')]



class account_move(osv.osv):
    _inherit = 'account.move'

    _columns = {
        'unique_piece_id': fields.char('Piece ID', size=64, readonly=True, help='Piece ID'),
    }

    _sql_constraints = [
        ('unique_piece_id_unique', 'unique(unique_piece_id)',
         'THE FIELD PIECE ID CORRESPONDING TO MOVE MUST BE UNIQUE !')
    ]

    def post(self, cr, uid, ids, context=None):
        obj_sequence = self.pool.get('ir.sequence')
        res = super(account_move, self).post(cr, uid, ids, context=context)
        for move in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, [move.id], {'unique_piece_id': self.pool.get('ir.sequence').get(cr, uid, 'z.fr.move.seq')})
        return res

account_move()


class account_move_line(osv.osv):
    _inherit = "account.move.line"

    _columns = {
        'unique_piece_id': fields.related('move_id','unique_piece_id', type='char', relation='account.move', help='Piece ID', string='Piece ID'),
    }

    # Allow update move if reconciled false
    def _update_check(self, cr, uid, ids, context=None):
        done = {}
        for line in self.browse(cr, uid, ids, context=context):
            err_msg = ('Move name (id): %s (%s)') % (line.move_id.name, str(line.move_id.id))
#            if line.move_id.state <> 'draft' and (not line.journal_id.entry_posted):
#                raise osv.except_osv(_('Error!'), _('You cannot do this modification on a confirmed entry. You can just change some non legal fields or you must unconfirm the journal entry first.\n%s.') % err_msg)
            if line.reconcile_id:
                raise osv.except_osv(_('Error!'), _('You cannot do this modification on a reconciled entry. You can just change some non legal fields or you must unreconcile first.\n%s.') % err_msg)
            t = (line.journal_id.id, line.period_id.id)
            if t not in done:
                self._update_journal_check(cr, uid, line.journal_id.id, line.period_id.id, context)
                done[t] = True
        return True

account_move_line()



class z_fr_move_seq_config(osv.osv_memory):

    _name = 'z.fr.move.seq.config'
    _inherit = 'res.config'

    _columns = {
        'generate_ref': fields.selection(GENERATE_REFS, 'Generate Move Sequence', required=True),
    }

    def execute(self, cr, uid, ids, context=None):
        for config in self.read(cr, uid, ids, ['generate_ref']):
            move_ids = []
            if config['generate_ref'] == 'all':
                move_ids += self.pool.get(
                    'account.move').search(cr, uid, [], order='id asc', context=None)
            elif config['generate_ref'] == 'empty':
                move_ids += self.pool.get('account.move').search(
                    cr, uid, ['|', ('unique_piece_id', '=', False), ('unique_piece_id', '=', '')], order='id asc', context=None)

            for move_id in move_ids:
                m_ids = self.pool.get('account.move')
                m_id = m_ids.browse(cr, uid, move_id, context=context)
                # if m_id.unique_piece_id == False:
                seq_id = 'z.fr.move.seq'

                self.pool.get('account.move').\
                    write(cr, uid, [move_id],
                          {'unique_piece_id': self.pool.get(
                              'ir.sequence').get(cr, uid, seq_id)}

                          )

            move_ids = []
            move_ids += self.pool.get('account.move').search(
                cr, uid, [('unique_piece_id', '=', False)], order='id asc', context=None)
            move_ids += self.pool.get('account.move').search(
                cr, uid, [('unique_piece_id', '=', '')], order='id asc', context=None)
            if move_ids:
                raise osv.except_osv(
                    'Error', 'There is empty unique_piece_id !')

            duplicates = cr.execute("""
                SELECT COUNT(unique_piece_id)
                FROM account_move
                GROUP BY unique_piece_id
                HAVING ( COUNT(unique_piece_id) > 1 )
            """)
            if duplicates:
                raise osv.except_osv(
                    'Error', 'There is duplicates unique piece id !')

        return True

z_fr_move_seq_config()
