# Copyright (c) 2013, Indictranstech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = [], []
	columns = get_colums(filters)
	data = get_data(filters)
	return columns, data

def get_data(filters):
	if filters:
	 	return frappe.db.sql("""select so.name,so.customer,so.company,so.transaction_date,so.delivery_date,so.contact_person,so.customer_address,
	 							so.po_no,so.grand_total,so_item.item_name,so_item.item_group,
  								so_item.description,so_item.stock_uom,
  								so_item.qty,so_item.qty,
  								so_item.rate,so_item.base_net_rate,	
  								so_item.amount,so_item.base_net_amount  
								from
									`tabSales Order` so,`tabSales Order Item` so_item
								where
									so.name = '{0}' and so_item.parent ='{1}' and (so.status ='Draft' or so.status = 'To Deliver and Bill')
								order by so.name desc""".format(filters.name,filters.name),as_list=1)
	else:
		# sales_ordres = frappe.db.sql("""select so.name from `tabSales Order` so where so.status = 'Draft' or 
		# 		so.status = 'To Deliver and Bill'""",as_dict=1)
		# print "sales_ordres",sales_ordres
		data=[]
		total_row = [[u'', u'', u'', '','', u'', u'', u'',0.0, u'', u'', u'', u'',0.0,0.0,0.0,0.0, 0.0,0.0]]
		last_row = [[u'', u'', u'', '','', u'', u'', u'',0.0, u'', u'', u'', u'',0.0,0.0,0.0,0.0, 0.0,0.0]]
		sales_orders = frappe.db.sql("select so.name from `tabSales Order` so where so.status = 'Draft' or so.status = 'To Deliver and Bill'""",as_dict=1)
		for order in sales_orders:
			print "orders",order
			data1 = []
			data1 = frappe.db.sql("""select so.name,so.customer,so.company,so.transaction_date,so.delivery_date,so.contact_person,so.customer_address,
	 							so.po_no,so.grand_total,so_item.item_name,so_item.item_group,
  								so_item.description,so_item.stock_uom,
  								so_item.qty,so_item.qty,
  								so_item.rate,so_item.base_net_rate,	
  								so_item.amount,so_item.base_net_amount  
								from
									`tabSales Order` so,`tabSales Order Item` so_item
								where
									so.name = '{0}' and so_item.parent ='{1}' and (so.status ='Draft' or so.status = 'To Deliver and Bill')
								order by so.name desc""".format(order['name'],order['name']),as_list=1)
			print "data1",data1
			print "\n\n\_______________________"
			data.extend(data1)
			total_row = get_total_sales_amount(data1)
			last_row  = get_last_total(last_row,total_row)   
			data.extend(total_row)
		data.extend(last_row)
		return data
		# print "____________data",data
		# return frappe.db.sql("""select so.name,so.customer,so.company,so.transaction_date,so.delivery_date,so.contact_person,so.customer_address,so.po_no,
		# 		so.grand_total from `tabSales Order` so where so.status = 'Draft' or 
		# 		so.status = 'To Deliver and Bill'""",as_list=1) 


def get_colums(filters):
	columns =[ ("Sales Order") + ":Link/Sales Order:100",
				   ("Party") + ":Data:150",
				   ("Company") + ":Data:120",
				   ("Date") + ":Date:100",
				   ("Delivery Date") + ":Date:100",
				   ("Contact Person")+ " :Data:140",
				   ("Address")+":Data:180",
				   ("Ref No") + ":Data:140",
				   ("Amount") + ":Currency:120",
				   ("Item Name") + ":Data:100" ,
				   ("item_group") + ":Data:100",
				   ("Description") + ":Data:100",
				   ("UOM") + ":Data:50",
				   ("Qty") + ":Float:50" , 
				   ("Pending") + ":Float:60",
				   ("Rate") + ":Currency:120",
				   ("Net Rate") + ":Currency:120", 
		  		   ("Amount") + ":Currency:80",
		  		   ("Net Amount") + ":Currency:80" 
			 ]
				  	
	return columns

def get_total_sales_amount(item_list):
	amount = 0.0
	qty = 0.0
	pending_qty = 0.0
	rate = 0.0
	net_rate = 0.0
	amount1 = 0.0
	net_amount =0.0
	for item in item_list:
		amount = amount +float(item[8])
		qty = qty + float(item[13])
		pending_qty = pending_qty + float(item[14])
		rate = rate + float(item[15])
		net_rate = net_rate + float(item[16])
		amount1 =amount1 + float(item[17])
		net_amount = net_amount + float (item[18])
		
	return [[u'', u'', u'', '','', u'', u'', u'',amount, u'', u'', u'', u'',qty,pending_qty,rate,net_rate, amount1, net_amount]]

def get_last_total(last_row,item_list):
	
	amount = float(last_row[0][8])
	qty = float(last_row[0][13])
	pending_qty = float(last_row[0][14])
	rate = float(last_row[0][15])
	net_rate = float(last_row[0][16])
	amount1 = float(last_row[0][17])
	net_amount = float(last_row[0][18])


	for item in item_list:
		amount = amount +float(item[8])
		qty = qty + float(item[13])
		pending_qty = pending_qty + float(item[14])
		rate = rate + float(item[15])
		net_rate = net_rate + float(item[16])
		amount1 =amount1 + float(item[17])
		net_amount = net_amount + float (item[18])
		
	return [[u'', u'', u'', '','', u'', u'', u'',amount, u'', u'', u'', u'',qty,pending_qty,rate,net_rate, amount1, net_amount]]
