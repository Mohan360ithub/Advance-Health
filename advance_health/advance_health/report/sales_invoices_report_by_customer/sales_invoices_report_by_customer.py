import frappe
 
def execute(filters=None):
    columns = [
        {"label": "Customer ID", "fieldname": "customer_id", "fieldtype": "Link", "options": "Customer","width":200},
        {"label": "Customer Name", "fieldname": "customer_name", "fieldtype": "Data","width":200},
        {"label": "Sales Invoice IDs", "fieldname": "sales_invoice_ids", "fieldtype": "Data","width":200},
        {"label": "Total Sales Invoices", "fieldname": "total_invoices", "fieldtype": "Int","width":100},
        {"label": "Payment Entry IDs", "fieldname": "payment_entry_ids", "fieldtype": "Data","width":200},
        {"label": "Total Payment Entries", "fieldname": "total_payments", "fieldtype": "Int","width":100}
    ]
    
    data = []
 
    customers = frappe.get_all("Customer", filters={"disabled": 0})
    for customer in customers:
        customer_name = frappe.get_value("Customer", customer.name, "customer_name")
        sales_invoices = frappe.get_all("Sales Invoice", filters={"customer": customer.name}, fields=["name"])
        sales_invoice_ids = ", ".join([si.name for si in sales_invoices])
        total_invoices = len(sales_invoices)
        
        payment_entries = frappe.get_all("Payment Entry", filters={"party_type": "Customer", "party": customer.name}, fields=["name"])
        payment_entry_ids = ", ".join([pe.name for pe in payment_entries])
        total_payments = len(payment_entries)
        
        data.append({"customer_id": customer.name,
                     "customer_name": customer_name,
                     "total_invoices": total_invoices,
                     "sales_invoice_ids": sales_invoice_ids,
                     "total_payments": total_payments,
                     "payment_entry_ids": payment_entry_ids})
 
    return columns, data
