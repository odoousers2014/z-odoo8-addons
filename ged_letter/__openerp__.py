# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
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
{
    "name": "Ged Letters",
    "version": "0.9",
    "depends": ['base',
                'contacts',
                'document',
                'report',
                ],
    "author": "Zuher ELMAS",
    "category": "knowledge",
    "description": """
        This module provide to manage write, sent and receipt letter from your partners
    """,
    "data": ['ged_letter_sequence.xml',
             'ged_letter_view.xml',
             'ged_letter_data.xml',
             'ged_letter_report.xml',
             'partner_view.xml',
             'res_users_view.xml',
             # 'ged_letter_sent_workflow.xml',
             # 'ged_letter_receipt_workflow.xml',
             'wizard/ged_letter_reply.xml',
             # 'security/ged_letter_security.xml',
             # 'security/ir.model.access.csv',
             'view/report_ged_letter.xml',
             'data/ged_letter_mail.xml'

             ],
    'installable': True,
    'active': False,
}
