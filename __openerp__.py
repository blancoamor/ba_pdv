{
    'name': 'Blancoamor - PDV Customization',
    'category': 'POS',
    'version': '0.1',
    'depends': ['base','product','sale','ba_sales'],
    'data': [
	#'security/ir.model.access.csv',
	#'security/security.xml',
	#'wizard/wizard_view.xml',
	'pdv_view.xml',
    ],
    'demo': [
    ],
    'qweb': [],
    'installable': True,
}
