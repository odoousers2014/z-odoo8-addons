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
import datetime

from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import netsvc

class ged_letter_reply_wizard (osv.osv_memory):
    _name = "ged.letter.reply.wizard"
    _description = "Reply letter"

    def view_init(self, cr, uid, fields_list, context=None):

        if context is None:
            context = {}
        res = super(ged_letter_reply_wizard, self).view_init(cr, uid, fields_list, context=context)
        record_id = context and context.get('active_id', False)
        if record_id:
            reply_obj = self.pool.get('ged.letter')
            reply = reply_obj.browse(cr, uid, record_id, context=context)
            if reply.state not in ['done','draft']:
                raise osv.except_osv(_('Warning!'), _("You may only reply that are Confirmed, or Done!"))
        return res

    def create_reply(self, cr, uid, ids, context=None):

        if context is None:
            context = {}
        record_id = context and context.get('active_id', False) or False
        let_obj = self.pool.get('ged.letter')
        let_discussion_obj = self.pool.get('ged.discussion.letter')
        data_obj = self.pool.get('letter.reply.wizard.memory')
        act_obj = self.pool.get('ir.actions.act_window')
        model_obj = self.pool.get('ir.model.data')
        wf_service = netsvc.LocalService("workflow")
        let = let_obj.browse(cr, uid, record_id, context=context)
        data = self.read(cr, uid, ids[0], context=context)

        if let.type =='sent':
            new_type = 'receipt'
            seq_obj_name = 'ged_letter_receipt'
        elif let.type =='receipt':
            new_type = 'sent'
            seq_obj_name = 'ged_letter_sent'

        letter_name = self.pool.get('ir.sequence').get(cr, uid, seq_obj_name)

        #sent_cat_ids[let.category_ids] = [(6, 0, let_receipt.category_ids)]
        if let.discussion_id:
            discussion = let.discussion_id.id

        if not let.discussion_id:
            vals = {'date': datetime.datetime.today(),}
            discussion = let_discussion_obj.create(cr, uid, vals, context=context)

            if discussion:
                grp_vals = {'discussion_id': discussion,}
                let_wrt = let.write(grp_vals)


        if let.type =='receipt':
            cat = let_obj.browse(cr, uid, record_id, context=context)
            cat_ids = [category_id.id for category_id in cat.category_id]

            letter_data = {
                    'name': letter_name,
                    'origin_id': record_id,
                    'state':'draft',
                    'date': datetime.datetime.today(),
                    'type': new_type,
                    'object': let.subject,
                    'category_id': [(6, 0, cat_ids)],
                    'transmission_type_id': let.transmission_type_id.id,
                    'your_ref': let.your_ref,
                    'discussion_id': discussion,
                    'partner_id': let.partner_id.id,
                    'company_id': let.company_id.id,

                }
            let_id = let_obj.create(cr, uid, letter_data, context=context)

            # cr.execute('insert into letter_sent_receipt_rel (letter_sent_id,letter_receipt_id) values (%s,%s)', (let_id, let_receipt.id))

        if let.type =='sent':
            cat = let_obj.browse(cr, uid, record_id, context=context)
            cat_ids = [category_id.id for category_id in cat.category_id]

            letter_data = {
                    'name': letter_name,
                    'origin_id': record_id,
                    'state':'draft',
                    'date': datetime.datetime.today(),
                    'type': new_type,
                    'object': let.subject,
                    'category_id': [(6, 0, cat_ids)],
                    'transmission_type_id': let.transmission_type_id.id,
                    'your_ref': let.your_ref,
                    'discussion_id': discussion,
                    'partner_id': let.partner_id.id,
                    'company_id': let.company_id.id,

                }
            let_id = let_obj.create(cr, uid, letter_data, context=context)

            # cr.execute('insert into letter_sent_receipt_rel (letter_sent_id,letter_receipt_id) values (%s,%s)', (let_sent.id, let_id))

        res = let_id

        # model_list = {
        # 'sent': 'letter.sent',
        # 'receipt': 'letter.receipt',
        # }

        return {
            'domain': "[('id', 'in', ["+str(res)+"])]",
            'name': _('Letter'),
            'view_type':'form',
            'view_mode':'tree,form',
            'res_model': 'ged.letter',
            'type':'ir.actions.act_window',
            'context':context,
        }




ged_letter_reply_wizard()

