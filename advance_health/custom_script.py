import frappe

@frappe.whitelist()
def share_lead_with_user(lead_name, user):
    frappe.share.add('Lead', lead_name, user, read=1, write=1)
    return "Success"
    
    
    


@frappe.whitelist()
def delete_all_data_import_logs():
    try:
        frappe.db.sql('DELETE FROM `tabData Import Log`')
        return {"message": "All entries in Data Import Log deleted successfully"}
    except Exception as e:
        return {"error": str(e)}



@frappe.whitelist()
def delete_all_data_import_logs_lead():
    try:
        frappe.db.sql('DELETE FROM `tabLead`')
        return {"message": "All entries in Data Import Log deleted successfully"}
    except Exception as e:
        return {"error": str(e)}


@frappe.whitelist()
def delete_all_data_import_logs_Contact():
    try:
        frappe.db.sql('DELETE FROM `tabContact`')
        return {"message": "All entries in Data Import Log deleted successfully"}
    except Exception as e:
        return {"error": str(e)}
        
        
        
        
@frappe.whitelist()
def delete_all_data_import_logs_Customer():
    try:
        frappe.db.sql('DELETE FROM `tabCustomer`')
        return {"message": "All entries in Data Import Log deleted successfully"}
    except Exception as e:
        return {"error": str(e)}
        
        
        
        
        
        
        
       
@frappe.whitelist()
def create_todo(date, description, lead_name, lead_id, assign_to=None, category=None):
    todo = frappe.get_doc({
        'doctype': 'ToDo',
        'date': date,
        'allocated_to': assign_to,
        'description': description,
        'custom_category': category,
        'reference_type': "Lead",
        'reference_name': lead_id,
        'custom_lead_id1':lead_id,
        'custom_lead_name': lead_name
    })
    todo.insert(ignore_permissions=True)

    return todo.name


@frappe.whitelist()
def get_open_activities(lead_id):
    # Fetch open ToDos
    todos = frappe.get_all('Lead Follow Up', filters={'status': 'Open','lead_id':lead_id}, fields=['name', 'date', 'description','allocated_to','custom_category'])
    return todos
    
    
    
    
@frappe.whitelist()
def close_todo(todo_name):
    try:
        # Load the ToDo
        todo = frappe.get_doc('Lead Follow Up', todo_name)
        
        # Set the status to 'Closed'
        todo.status = 'Closed'
        
        # Save the changes
        todo.save()
        
        return True
    except frappe.DoesNotExistError:
        frappe.msgprint(f"ToDo {todo_name} not found.")
        return False
    except Exception as e:
        frappe.msgprint(f"Error closing ToDo: {str(e)}")
        return False
        
        
        
        
        
        
        
       
import frappe
from frappe import _


import frappe

@frappe.whitelist()
def sync_lead_records_background():
    frappe.enqueue("advance_health.custom_script.sync_lead_records", queue='long')

def sync_lead_records():
    try:
        # Fetch all lead records
        lead_records = frappe.get_all('Lead', filters={'custom_assign_to': ('is', 'set')}, fields=['name', 'custom_assign_to'])

        # Share each lead record with custom_assign_to user
        for lead in lead_records:
            custom_assign_to = lead.get('custom_assign_to')

            if custom_assign_to:
                # Share the lead record with custom_assign_to user
                frappe.share.add('Lead', lead.name, custom_assign_to, read=1, write=1)

        return True
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), frappe._('Sync Lead Records Error'))
        return False

   
   
   
@frappe.whitelist()
def get_todo_details(todo_name):
    todo = frappe.get_doc('Lead Follow Up', todo_name)
    return {
        'description': todo.description,
        'custom_category': todo.custom_category,
        'date': todo.date,
        'allocated_to': todo.allocated_to
        # Add more fields as needed
    }     
    
    
    
    
@frappe.whitelist()
def update_todo(todo_name, updated_values):
    todo = frappe.get_doc('Lead Follow Up', todo_name)

    # Parse the JSON string into a dictionary
    updated_values_dict = frappe.parse_json(updated_values)

    # Update the ToDo with the edited values
    todo.update(updated_values_dict)
    todo.save()
    return True
    
    
    
    


@frappe.whitelist()
def check_followed_up_leads_que():
    frappe.enqueue("advance_health.custom_script.check_followed_up_leads", queue='long')

@frappe.whitelist()
def check_followed_up_leads():
    try:
        # Fetch all leads
        leads = frappe.get_all('Lead', pluck='name')

        # Check followed up for each lead
        for lead_id in leads:
            lead_follow_up_exists = frappe.get_all('Lead Follow Up', filters={'lead_id': lead_id})
            if lead_follow_up_exists:
                # Set the 'followed_up' checkbox in the Lead to 1
                frappe.db.set_value('Lead', lead_id, 'followed_up', 1)

        return True
    except Exception as e:
        frappe.log_error(str(e))
        return False



import frappe
from frappe.utils import getdate, add_days

@frappe.whitelist()
def create_lead_follow_up_for_leads_without_follow_up_background():
    try:
        frappe.enqueue("advance_health.custom_script.create_lead_follow_up_for_leads_without_follow_up", queue='long')
        return True
    except Exception as e:
        frappe.log_error(f"Failed to add task to the queue: {str(e)}")
        return False

@frappe.whitelist()
def create_lead_follow_up_for_leads_without_follow_up():
    """
    Create Lead Follow Up records for leads without any follow-up records.
    """
    try:
        leads_without_follow_up = frappe.get_all('Lead', filters={'name': ('not in', get_leads_with_follow_up_ids()), 'status': 'Lead'},
                                                 fields=['name', 'custom_assign_to'])
        tomorrow_date = add_days(getdate(), 1)
        for lead in leads_without_follow_up:
            lead_id = lead['name']
            custom_assign_to = lead['custom_assign_to']
            if create_lead_follow_up(lead_id, tomorrow_date, custom_assign_to):
                continue
            else:
                return False

        return True
    except Exception as e:
        frappe.log_error(f"Failed to create Lead Follow Up records: {str(e)}")
        return False

def get_leads_with_follow_up_ids():
    """
    Get lead IDs with existing follow-up records.
    """
    leads_with_follow_up = frappe.get_all('Lead Follow Up', filters={'lead_id': ('!=', '')}, fields=['lead_id'])
    return [lead['lead_id'] for lead in leads_with_follow_up]

def create_lead_follow_up(lead_id, follow_up_date, custom_assign_to):
    """
    Create Lead Follow Up record for the given lead ID.
    """
    try:
        lead_follow_up = frappe.new_doc('Lead Follow Up')
        lead_follow_up.lead_id = lead_id
        lead_follow_up.date = follow_up_date
        lead_follow_up.custom_category = 'Call'
        lead_follow_up.description = 'Call'
        lead_follow_up.save(ignore_permissions=True)

        # Share Lead Follow Up with custom_assign_to
        if custom_assign_to:
            frappe.share.add('Lead Follow Up', lead_follow_up.name, custom_assign_to, read=1, write=1)
        return True
    except Exception as e:
        frappe.log_error(f"Failed to create Lead Follow Up for lead {lead_id}: {str(e)}")
        return False





import frappe

@frappe.whitelist()
def get_leads_by_last_10_digits():
    # Fetch all leads
    leads = frappe.get_all("Lead", fields=["name", "mobile_no"])
    
    # Dictionary to store matching leads
    matching_leads = {}
    
    # Iterate through leads
    for lead in leads:
        mobile_no = lead.get("mobile_no")
        if mobile_no and len(mobile_no) >= 10:  # Ensure mobile number is at least 10 digits long
            last_10_digits = mobile_no[-10:]
            if last_10_digits in matching_leads:
                matching_leads[last_10_digits].append(lead)
            else:
                matching_leads[last_10_digits] = [lead]

    # Filter leads with more than one match
    matching_leads_multiple = {mob: leads for mob, leads in matching_leads.items() if len(leads) > 1}

    return matching_leads_multiple





import frappe
 
@frappe.whitelist()
def get_payment_entries(customer, invoice_name):
    # Fetch payment entries based on customer and invoice name
    payment_entries = frappe.get_list("Payment Entry",
                                      filters={"party_type": "Customer", "party": customer, "reference_doctype": "Sales Invoice", "reference_name": invoice_name},
                                      fields=["name", "posting_date", "paid_amount", "mode_of_payment", "references.allocated_amount", "references.outstanding_amount", "references.payment_term", "references.total_allocated_amount"])
 
    # Return the payment entries as JSON string
    return payment_entries
 






@frappe.whitelist(allow_guest=True)
def reallocate_lead(lead_name, custom_assign_to):
    # print(custom_assign_to)
    res2=remove_lead_share(lead_name)
    if custom_assign_to:
        res1=share_lead_with_user(lead_name, custom_assign_to)
    if res2:
        if custom_assign_to and res1:
            return "Success"
        elif custom_assign_to:
            return "Failed"
        else:
            # print("Success")
            return "Success"
        
@frappe.whitelist(allow_guest=True)
def share_lead_with_user(lead_name, user):
    frappe.share.add('Lead', lead_name, user, read=1, write=1)
    return "Success"
 
@frappe.whitelist(allow_guest=True)
def remove_lead_share(lead_name):
    shares = frappe.share.get_users("Lead", lead_name)
    # print("Hello",shares,lead_name)
    for sh in shares:
        frappe.share.remove("Lead", lead_name, sh.user)
        # print(sh.user)
    return "Success"
 
#lead Follow Up
import frappe

@frappe.whitelist(allow_guest=True)
def reallocate_lead_follow_up(lead_name, allocated_to, lead_id):
    # Remove existing lead sharing
    res2 = remove_lead_sharing(lead_name)
    # res3 = remove_lead_sharing1(lead_id)

    if allocated_to:
        # Share lead follow-up with the new user
        res1 = share_lead_follow_up_with_user(lead_name, allocated_to)
        res4 = share_lead_follow_up_with_user1(lead_id, allocated_to)

        if res2 and res1:
            return "Success"
        elif allocated_to:
            return "Failed"
        else:
            return "Success"
    else:
        return "Success" if res2 else "Failed"

@frappe.whitelist()
def share_lead_follow_up_with_user(lead_name, allocated_to):
    frappe.share.add('Lead Follow Up', lead_name, allocated_to, read=1, write=1)
    return "Success"

@frappe.whitelist()
def share_lead_follow_up_with_user1(lead_id, allocated_to):
    frappe.share.add('Lead', lead_id, allocated_to, read=1, write=1)
    return "Success"

@frappe.whitelist(allow_guest=True)
def remove_lead_sharing(lead_name):
    shares = frappe.share.get_users("Lead Follow Up", lead_name)
    for sh in shares:
        frappe.share.remove("Lead Follow Up", lead_name, sh.user)
    return "Success"

@frappe.whitelist(allow_guest=True)
def remove_lead_sharing1(lead_id):
    shares = frappe.share.get_users("Lead", lead_id)
    for sh in shares:
        frappe.share.remove("Lead", lead_id, sh.user)
    return "Success"


@frappe.whitelist()
def send_admission_form(customer_id, email_id, mobile_no=None):
    
    # Constructing the message with the link including the customer ID, custom_customer_email, and email_id
    admission_form_link = f"/admission-form/new?customer_id={customer_id}&email_id={email_id}&contact_no={mobile_no}"
    message = f"""<html>
            <body>
                <p>Thank you for choosing Advanced Health. We appreciate your interest in our services.</p>
                <p>To proceed with your admission, please fill out the <a href="{admission_form_link}">Admission Form</a> with accurate information. Your cooperation in providing detailed and precise information will enable us to better understand your needs and provide you with the best possible care.</p>
                <p>If you encounter any difficulties or have any questions regarding the form, please don't hesitate to contact us.</p>
                <p>We look forward to welcoming you as part of the Advanced Health community.</p>
                <p>Best regards,<br> drravi@idealcure4u.com,<br> 9373101813,<br> Advanced Health Team</p>
            </body>
            </html>"""
 
    
    # Sample code to send email
    subject = "Admission Form"
    recipients = [email_id]
    
    
    frappe.sendmail(
        recipients=recipients,
        subject=subject,
        message=message,
        reference_doctype='Customer',  # Adjust if necessary
        reference_name=customer_id  # Adjust if necessary
    )
 
    # You can add more logic here as per your requirements
 
    return _("Admission form sent successfully.")
 
 
 
 
 
@frappe.whitelist(allow_guest=True)
def validate_overlap(customer_id, from_date, to_date):
    existing_forms = frappe.get_all("Admission Form", filters={
        "customer_id": customer_id,
        "from_date": ("<=", to_date),
        "to_date": (">=", from_date)
    })
 
    if existing_forms:
        return "We already have a form submitted for the same time slot you're requesting."
 
    return None
 
@frappe.whitelist()
def validate_duplicate_before_form(customer_id, form_id):
    # Check if there's already a form with the same customer_id and form_id
    existing_form = frappe.db.exists("Before starting the Treatment", {"customer_id": customer_id, "form_id": form_id})
 
    if existing_form:
        return "A form has been already exists for this customer ."
    else:
        return None  # No duplicate form found, validation passed
 
@frappe.whitelist()
def validate_duplicate_after_form(customer_id, form_id):
    # Check if there's already a form with the same customer_id and form_id
    existing_form = frappe.db.exists("Before starting the Treatment", {"customer_id": customer_id, "form_id": form_id})
 
    if existing_form:
        return "A form has been already exists for this customer ."
    else:
        return None  # No duplicate form found, validation passed
    
    
    
    
    

