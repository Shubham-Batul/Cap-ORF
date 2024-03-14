{
    'name':'Cap ORF',
    'author': 'Captivea',
    'summary': 'Cap ORF module',
    'depends':['base','product','purchase','portal','mail'],
    'data':[
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/purchase_view.xml',
        'views/order_line.xml',
        'views/purchase_inherit.xml',
        'views/portal.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',

}