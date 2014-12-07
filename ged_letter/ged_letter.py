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

from datetime import datetime, timedelta
import itertools
from lxml import etree

from openerp import models, fields, api, _
from openerp.osv import osv
from openerp.exceptions import except_orm, Warning, RedirectWarning

# mapping letter
TYPE2LETTER = {
    'in_letter': 'in_letter',           # In Letter
    'out_letter': 'out_letter',        # Out Letter
}

MAGIC_COLUMNS = ('id', 'create_uid', 'create_date', 'write_uid', 'write_date')


class ged_letter_tags(models.Model):

    @api.v7
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

    @api.multi
    def _name_get_fnc(self, field_name, arg):
        return dict(self.name_get())

    _description = 'Letter Tags'
    _name = 'ged.letter.tags'

    name = fields.Char(string='Name', size=64, required=True, readonly=False)
    parent_id = fields.Many2one('ged.letter.tags', string='Category Parent')
    complete_name = fields.Char(string='Name', compute='_name_get_fnc',)
    child_ids = fields.One2many(
        'ged.letter.tags', 'parent_id', string='Child Categories')
    abrev = fields.Char(
        string='Abbreviation', size=5, required=True, readonly=False)
    active = fields.Boolean(
        string='Active', help="The active field allows you to hide the category without removing it.")
    parent_left = fields.Integer(string='Left Parent', select=True)
    parent_right = fields.Integer(string='Right Parent', select=True)
    letter_ids = fields.Many2many(
        'ged.letter', string='Letters')

    _sql_constraints = [
        ('abrev_unique', 'unique(abrev)', 'THE ABBREVIATION MUST BE UNIQUE !')
    ]

    # _parent_name = "parent_id"
    _parent_store = True
    _parent_order = 'name'
    _order = 'parent_left'

    _constraints = [
        (osv.osv._check_recursion,
         'Error ! You can not create recursive categories.', ['parent_id'])
    ]


class ged_letter_transmission(models.Model):
    _name = 'ged.letter.transmission'
    _description = 'ged_letter_transmission'

    ref = fields.Char('Code', size=64, required=True, readonly=False)
    name = fields.Char('Name', size=254, required=True, readonly=False)
    acknowledgment = fields.Boolean('Acknowledgment', required=False)


class ged_letter_template(models.Model):
    _name = 'ged.letter.template'
    _description = 'Letter Template'

    name = fields.Char(string='Name', size=64, required=True, readonly=False)
    content = fields.Html(string='Letter template')

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'THE FIELD NAME MUST BE UNIQUE !')
    ]


class closing_formula(models.Model):
    _name = 'closing.formula'
    _description = 'Closing formula template'

    name = fields.Char(string='Name', size=64, required=True, readonly=False)
    content = fields.Html(string='Closing Formula')

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'THE FIELD NAME MUST BE UNIQUE !')
    ]


class ged_letter(models.Model):

    _name = 'ged.letter'
    _inherit = ['mail.thread']
    _description = 'GED Letter'
    _track = {
        'state': {
            'ged_letter.lt_assign': lambda self, cr, uid, obj, ctx=None: obj['state'] in ['pending_confirm'],
            'ged_letter.lt_reject': lambda self, cr, uid, obj, ctx=None: obj['state'] in ['reject'],
            'ged_letter.lt_confirmed': lambda self, cr, uid, obj, ctx=None: obj['state'] in ['confirmed'],
            'ged_letter.lt_sent': lambda self, cr, uid, obj, ctx=None: obj['state'] in ['sent']
        },
    }
    _order = "id desc"

    @api.model
    def create(self, vals):
        if ('name' not in vals) or (vals.get('name') == '/'):
            ged_type = vals.get('type')
            if ged_type == 'receipt':
                seq_obj_name = 'ged_letter_receipt'

            if ged_type == 'sent':
                seq_obj_name = 'ged_letter_sent'

            vals['name'] = self.env['ir.sequence'].get(seq_obj_name)

        new_id = super(ged_letter, self).create(vals)
        return new_id

    name = fields.Char(
        string='Reference', size=64, required=False, readonly=True, default='/',)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('write_finish', 'Write Finish'),
        ('pending_confirm', 'Pending Confirm'),
        ('reject', 'Reject'),
        ('confirmed', 'Confirmed'),
        ('sent', 'Sent'),
        ('recipiant_receipt', 'Waiting Receipt'),
        ('reply', 'Replied'),
        ('cancel', 'Cancel letter'),
        ('done', 'Done'),
    ], string='Status', readonly=True, track_visibility='onchange', index=True, default='draft', copy=False)
    type = fields.Selection([('sent', 'Sent letter'), ('receipt', 'Receipt letter')],
                            string='Letter Transmission Type', required=True, select=True, help="Sent or receipt transmission type.")
    partner_id = fields.Many2one('res.partner', string='Recipient', readonly=True, states={'draft': [
                                 ('readonly', False)]}, required=True, change_default=True, select=True, track_visibility='always')
    for_is = fields.Char(string='For is', size=254, required=False, readonly=False, states={
                         'done': [('readonly', True)], 'cancel': [('readonly', True)]},)
    date = fields.Date(string='Date letter', required=True, readonly=True, states={'draft': [('readonly', False)], 'write_finish': [
                       ('readonly', False)]}, help="Indicate the time of writing the letter. This should appear in the address")
    transmission_type_id = fields.Many2one(
        'ged.letter.transmission', string='Transmission Type', required=True)
    subject = fields.Char(string='Subject', size=254, required=False, readonly=True, states={
        'draft': [('readonly', False)]})
    content = fields.Html(
        string='Contents of the letter', readonly=True, states={'draft': [('readonly', False)]})
    user_id = fields.Many2one(
        'res.users', string='Editor', select=True, readonly=True, track_visibility='onchange', default=lambda self: self.env.user)
    user_write_signature = fields.Many2one('res.users', string='User signature', select=True, readonly=True, states={
                                           'draft': [('readonly', False)], 'write_finish': [('readonly', False)]}, track_visibility='onchange', default=lambda self: self.env.user)
    confirmed_user = fields.Boolean(
        string='Confirmed by Signatory', required=False, readonly=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True, states={'draft': [(
        'readonly', False)]}, change_default=True, default=lambda self: self.env['res.company']._company_default_get('ged.letter'))
    your_ref = fields.Char(string='Your Reference', size=64, required=False, readonly=True, states={
                           'draft': [('readonly', False)], 'write_finish': [('readonly', False)]})
    note = fields.Text(
        string='Notes', states={'done': [('readonly', True)], 'cancel': [('readonly', True)]})
    date_reply = fields.Date(
        string='Date reply', help="Indicate the date on which the letter was reply")
    date_sent = fields.Date(string='Date sent', readonly=True, states={'draft': [('invisible', True)], 'confirmed': [
                            ('readonly', False)]}, help="Indicate the date on which the letter was sent")
    date_recipient_receipt = fields.Date(
        string='Date received', help="Date with the letter sent by registered post with acknowledgment of receipt was received by the recipient")
    closing_formula = fields.Html(
        string='Clausing Formula', readonly=True, states={'draft': [('readonly', False)]})
    closing_formula_id = fields.Many2one('closing.formula', string='Clausing Formula Template', readonly=True, states={
                                         'draft': [('readonly', False)]}, track_visibility='onchange')
    ged_template_id = fields.Many2one('ged.letter.template', string='Model', readonly=True, states={
                                      'draft': [('readonly', False)]})

    origin_id = fields.Many2one('ged.letter', string='Origin', readonly=True, states={
                                'draft': [('readonly', False)]}, change_default=True)
    category_id = fields.Many2many('ged.letter.tags', string='Tags')
    rel_partner_id = fields.Many2many(
        'res.partner', string='Partners Concerned')
    attachments = fields.One2many(
        'ir.attachment', 'ged_letter_id', string='Attachments',  readonly=True)

    _sql_constraints = [
        ('name_unique', 'unique(name)',
         'THE FIELD NAME CORRESPONDING TO THE REFERENCE LETTER MUST BE UNIQUE !')
    ]

    @api.multi
    def unlink(self):
        for ged_let in self:
            if ged_let.state not in ('draft', 'cancel'):
                raise Warning(
                    _('You cannot delete an letter which is not draft or cancelled.'))

        return super(ged_letter, self).unlink()

    # def copy(self, cr, uid, id, default=None, context=None):
    #     if default is None:
    #         default = {}
    #     default = default.copy()
    #     letter_obj = self.browse(cr, uid, id, context=context)

    #     if ('name' not in default) or (letter_obj.name == '/'):
    #         seq_obj_name = 'letter.' + letter_obj.type
    #         default['name'] = self.pool.get(
    #             'ir.sequence').get(cr, uid, seq_obj_name)
    #         default['state'] = 'draft'
    #         default['date'] = fields.date.context_today(
    #             self, cr, uid, context=context),
    #     res = super(letter, self).copy(cr, uid, id, default, context)
    #     return res

    @api.model
    def fields_view_get(self, view_id=None, view_type=False, context=None, toolbar=False, submenu=False):
        context = self._context
        if view_type == 'form' and not view_id:
            mod_obj = self.pool.get('ir.model.data')
            if context.get('type') == "letter.sent":
                model, view_id = mod_obj.get_object_reference(
                    'ged_letter', 'ged_letter_sent_form')
            if context.get('type') == "letter.receipt":
                model, view_id = mod_obj.get_object_reference(
                    'ged_letter', 'ged_letter_receipt_form')
        return super(ged_letter, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)

    @api.multi
    def letter_print(self):
        """ Print the invoice and mark it as sent, so that we can see more
            easily the next step of the workflow
        """
        assert len(
            self) == 1, 'This option should only be used for a single id at a time.'
        self.sent = True
        return self.env['report'].get_action(self, 'ged_letter.report_ged_letter')

    @api.multi
    def action_draft(self):
        self.write({'state': 'draft', 'confirmed_user': False})
        self.delete_workflow()
        self.create_workflow()
        return True

    @api.multi
    def action_cancel(self):
        self.write({'state': 'cancel'})
        self._log_event(-1.0, 'Cancel Letter')
        return True

    @api.multi
    def _log_event(self, factor=1.0, name='New letter'):
        return True

    @api.multi
    def button_done(self):
        return self.write({'state': 'done'})

    @api.onchange('ged_template_id')
    def onchange_model(self):
        templ = self.ged_template_id

        if templ:
            self.content = templ.content

    @api.onchange('closing_formula_id')
    def onchange_closing_formula(self):
        cf_id = self.closing_formula_id

        if cf_id:
            self.closing_formula = cf_id.content

    @api.multi
    def button_sent(self):
        for let in self:
            if not let.date_sent:
                raise Warning(
                    _('Date sent !'), _('You need to insert date sent!'))
                date_today = datetime.now()
                res = self.write({'date_sent': date_today})

            if let.date_sent:
                if let.transmission_type_id.acknowledgment == True:
                    self.write({'state': 'recipiant_receipt'})

                if let.transmission_type_id.acknowledgment == False:
                    self.write({'state': 'sent'})
        return True

    @api.multi
    @api.depends('message_follower_ids')
    def button_ready_to_send(self):
        for let in self:
            uw = let.user_write_signature.id
            ur = let.user_id.id

            for follow in let.message_follower_ids:
                if follow and follow[0]:
                    msg = follow[0]

                if uw != msg:
                    self.message_subscribe(
                        [let.user_write_signature.partner_id.id])

            if uw == ur:
                self.write(
                    {'state': 'write_finish', 'confirmed_user': True})

            if uw != ur:
                self.write({'state': 'pending_confirm'})

        return True

    @api.multi
    def action_assign_validator(self):
        for let in self:
            uw = let.user_write_signature.id
            ur = let.user_id.id
            if uw != ur:
                self.write({'state': 'pending_confirm'})

        return True

    @api.multi
    def button_reject(self):
        for let in self:
            uw = let.user_write_signature.id
            ur = let.user_id.id

            if let.state in ('pending_confirm'):
                if uid != uw:
                    raise osv.except_osv(
                        _('Error!'), _('You can not reject this letter. The signatory should give its approval or reject.'))
                if uid == uw:
                    self.write(
                        {'state': 'reject', 'confirmed_user': False})
        return True

    @api.multi
    def button_confirm(self):
        user = self.env.user.id
        for let in self:
            uw = let.user_write_signature.id
            ur = let.user_id.id
            if let.state in ('write_finish'):
                if user != uw:
                    self.write(
                        {'state': 'pending_confirm', 'confirmed_user': False})
                if user == uw:
                    self.write({'state': 'confirmed', 'confirmed_user': True})

            if let.state in ('pending_confirm'):
                if user != uw:
                    raise osv.except_osv(
                        _('Error!'), _('You can not confirm this letter. The signatory should give its approval.'))
                if user == uw:
                    self.write({'state': 'confirmed', 'confirmed_user': True})
        return True

    @api.multi
    def button_confirmed_receipt(self):
        for let in self:
            if not let.date_recipient_receipt:
                raise Warning(
                    _('Date sent !'), _('You must insert the date of receipt of the letter.!'))

            if let.date_recipient_receipt:
                self.write({'state': 'done'})

        return True

    @api.multi
    def button_letter_in_confirm(self):
        for let in self:
            if not let.date:
                raise Warning(
                    _('Date sent !'), _('You must insert the date of receipt of the letter.!'))

            if let.date:
                self.write({'state': 'confirmed'})

        return True

    @api.multi
    def action_letter_sent_mail(self):
        """ Open a window to compose an email, with the edi letter template
            message loaded by default
        """
        assert len(
            self) == 1, 'This option should only be used for a single id at a time.'
        template = self.env.ref('ged_letter.email_template_edi_letter', False)
        compose_form = self.env.ref(
            'mail.email_compose_message_wizard_form', False)
        ctx = dict(
            default_model='ged.letter',
            default_res_id=self.id,
            default_use_template=bool(template),
            default_template_id=template.id,
            default_composition_mode='comment',
            mark_invoice_as_sent=True,
        )
        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }
