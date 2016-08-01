import logging
import psycopg2
import time
from datetime import datetime

from openerp import tools
from openerp.osv import fields, osv
from openerp.tools import float_is_zero
from openerp.tools.translate import _

import openerp.addons.decimal_precision as dp
import openerp.addons.product.product


class pos_order(osv.osv):
	_inherit = 'pos.order'

	def add_payment(self, cr, uid, order_id, data, context=None):
		import pdb;pdb.set_trace()
		if data['journal_id']:
			order = self.pool.get('pos.order').browse(cr,uid,context['active_id'])
			journal = self.pool.get('account.journal').browse(cr,uid,data['journal_id'][0])
			if journal.sale_cuotas_id:
				vals_line = {
					'product_id': journal.sale_cuotas_id.product_id.id,
					'order_id': context['active_id'],
					'display_name': journal.sale_cuotas_id.name,
					'qty': 1,
					'price_unit': journal.sale_cuotas_id.amount,
					'price_subtotal': journal.sale_cuotas_id.amount,
					}
				line_id = self.pool.get('pos.order.line').create(cr,uid,vals_line)
		return super(pos_order,self).add_payment(cr,uid,order_id,data,context)
