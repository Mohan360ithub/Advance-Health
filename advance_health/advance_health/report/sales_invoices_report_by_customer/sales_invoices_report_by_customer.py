import frappe

def execute(filters=None):
    # Define columns for the report
    columns = [
        {"label": "Customer Name", "fieldname": "customer_name", "fieldtype": "Data", "width": 200},
        {"label": "Sales Invoice ID", "fieldname": "sales_invoice_id", "fieldtype": "Link", "options": "Sales Invoice", "width": 200},
        {"label": "Grand Total", "fieldname": "grand_total", "fieldtype": "Currency", "width": 150},
        {"label": "Outstanding Amount", "fieldname": "outstanding_amount", "fieldtype": "Currency", "width": 150},
        {"label": "Paid Amount", "fieldname": "paid_amount", "fieldtype": "Currency", "width": 150}
    ]

    # Initialize an empty list to store data
    data = []

    # Get all active customers
    customers = frappe.get_all("Customer", filters={"disabled": 0})
    
    # Iterate through each customer
    for customer in customers:
        customer_name = frappe.get_value("Customer", customer.name, "customer_name")
        
        # Get all sales invoices related to the current customer
        sales_invoices = frappe.get_all("Sales Invoice", filters={"customer": customer.name}, fields=["name", "outstanding_amount", "grand_total"])
        
        # Iterate through each sales invoice
        for invoice in sales_invoices:
            # Calculate paid amount
            paid_amount = invoice["grand_total"] - invoice["outstanding_amount"]
            
            # Append invoice details to the data list
            data.append({
                "customer_name": customer_name,
                "sales_invoice_id": invoice["name"],
                "grand_total": invoice["grand_total"],
                "outstanding_amount": invoice["outstanding_amount"],
                "paid_amount": paid_amount
            })

    # Return columns and data
    return columns, data
