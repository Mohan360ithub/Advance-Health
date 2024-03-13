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
        
        
        
        
        
        
        
       
@frappe.whitelist()
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
        frappe.log_error(frappe.get_traceback(), _('Sync Lead Records Error'))
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



@frappe.whitelist()
def update_followed_up(lead_id):
    lead = frappe.get_doc("Lead", lead_id)
    
    if lead and lead.followed_up != 1:
        lead.followed_up = 1
        lead.save(ignore_permissions=True)  # Update the lead's followed_up field
        frappe.msgprint(_("Lead {0} marked as followed up.").format(lead_id))

