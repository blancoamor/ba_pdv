from openerp import models, fields, api, _
from openerp.osv import osv
from openerp.exceptions import except_orm, ValidationError
from StringIO import StringIO
import urllib2, httplib, urlparse, gzip, requests, json
import openerp.addons.decimal_precision as dp
import logging
import datetime
from openerp.fields import Date as newdate
from datetime import datetime

#Get the logger
_logger = logging.getLogger(__name__)

class sale_order(models.Model):
	_inherit = 'sale.order'

	@api.one
	def create_pdv_ticket(self):
		# Checks if a session is open
		session_id = self.env['pos.session'].search([('state','=','opened')])
		if not session_id:
			raise ValidationError('No hay sesion abierta')
		vals_pos_order = {
			'session_id': session_id.id,
			'name': self.name,
			'partner_id': self.partner_id.id,
			'location_id': session_id.config_id.stock_location_id.id,
			'user_id': self.user_id.id,
			'pos_reference': self.client_order_ref,	
			}
		pos_order = self.env['pos.order'].create(vals_pos_order)	
		for line in self.order_line:
			vals_line = {
				'order_id': pos_order.id,
				'discount': line.discount,
				'display_name': line.description,
				'name': line.name,
				'price_subtotal': line.price_subtotal,
				'price_unit': line.price_unit,
				'qty': line.product_uom_qty,
				'product_id': line.product_id.id,
				}
			pos_order_line = self.env['pos.order.line'].create(vals_line)
