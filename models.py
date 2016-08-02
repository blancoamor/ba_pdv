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

class pos_make_payment(models.TransientModel):
	_inherit = 'pos.make.payment'

	total_amount = fields.Float('Monto total con recargos')
	journal_id = fields.Many2one('account.journal',string='Payment Mode',required=True,domain=[('journal_user','=',True)])

	@api.onchange('journal_id')
	def change_journal_id(self):
		if self.journal_id.sale_cuotas_id:
			if self.journal_id.sale_cuotas_id.monto:
				self.total_amount = self.amount + self.journal_id.sale_cuotas_id.monto


class account_journal(models.Model):
	_inherit = 'account.journal'

	sale_cuotas_id = fields.Many2one('sale.cuotas')


class pos_order(models.Model):
	_inherit = 'pos.order'

	sale_order_id = fields.Many2one('sale.order')


class sale_order(models.Model):
	_inherit = 'sale.order'

	@api.one
	def create_pdv_ticket(self):
		# Checks if a session is open

		if self.ticket_id:
			raise ValidationError('Ya hay ticket creado para el pedido')
		if not self.user_id.pos_config:
			raise ValidationError('No existe sucursal definida para el usuario.\nPor favor contacte al administrador')
		session_id = self.env['pos.session'].search([('state','=','opened'),('config_id','=',self.user_id.pos_config.id)])
		if not session_id:
			raise ValidationError('No hay sesion abierta')
		vals_pos_order = {
			'session_id': session_id.id,
			'name': self.name,
			'partner_id': self.partner_id.id,
			'location_id': session_id.config_id.stock_location_id.id,
			'user_id': self.user_id.id,
			'pos_reference': self.client_order_ref,	
			'sale_order_id': self.id,
			}
		pos_order = self.env['pos.order'].create(vals_pos_order)	
		for line in self.order_line:
			vals_line = {
				'order_id': pos_order.id,
				'discount': line.discount,
				'display_name': line.name,
				'name': line.name,
				'price_subtotal': line.price_subtotal,
				'price_unit': line.price_unit,
				'qty': line.product_uom_qty,
				'product_id': line.product_id.id,
				}
			pos_order_line = self.env['pos.order.line'].create(vals_line)
		for picking in self.picking_ids:
			picking.action_cancel()


	ticket_id = fields.One2many(comodel_name='pos.order',inverse_name='sale_order_id')
