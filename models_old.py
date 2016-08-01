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
		return super(pos_order,self).add_payment(cr,uid,order_id,data,context)
