# Import necessary modules
import frappe
 
# Function to get data for all users except "sandesh@advancedhealth.in"
def get_all_users_data():
    # Fetch data for all users including Sandesh
    unwanted_users = ["Administrator", "Guest", "pankaj@360ithub.com", "mohan@360ithub.com","sandesh@advancedhealth.in"]
    users = frappe.get_all("User",
                            fields=["name", "full_name"],
                            filters={"name": ["not in", unwanted_users]})
 
    lead_follow_ups = frappe.get_all("Lead Follow Up", fields=["lead_id", "status"])
    lead_follow_ups_map = {}
    for fu in lead_follow_ups:
        if fu["lead_id"] not in lead_follow_ups_map:
            lead_follow_ups_map[fu["lead_id"]] = {}
            lead_follow_ups_map[fu["lead_id"]][fu["status"]] = 1
        else:
            if fu["status"] not in lead_follow_ups_map[fu["lead_id"]]:
                lead_follow_ups_map[fu["lead_id"]][fu["status"]] = 1
            else:
                lead_follow_ups_map[fu["lead_id"]][fu["status"]] += 1
 
    leads_with_assigned_to = frappe.get_all("Lead",
                        filters={"custom_assign_to": ("not in", [None])},
                        fields=["name", "custom_assign_to", "status"])
 
    user_dict = {i.name: {"full_name": i.full_name, "user": i.name, "lead": 0, "lost": 0, "followup": 0, "open_fu": 0, "closed_fu": 0, "converted": 0} for i in users}
 
    for lead in leads_with_assigned_to:
        if lead.custom_assign_to in user_dict:
            user_dict[lead.custom_assign_to]["lead"] += 1
            if lead["status"] == "Lost":
                user_dict[lead.custom_assign_to]["lost"] += 1
            if lead["status"] == "Converted":
                user_dict[lead.custom_assign_to]["converted"] += 1
            if lead.name in lead_follow_ups_map:
                fu = 0
                if "Open" in lead_follow_ups_map[lead.name]:
                    user_dict[lead.custom_assign_to]["open_fu"] += lead_follow_ups_map[lead.name]["Open"]
                    fu += lead_follow_ups_map[lead.name]["Open"]
                if "Closed" in lead_follow_ups_map[lead.name]:
                    user_dict[lead.custom_assign_to]["closed_fu"] += lead_follow_ups_map[lead.name]["Closed"]
                    fu += lead_follow_ups_map[lead.name]["Closed"]
                user_dict[lead.custom_assign_to]["followup"] += fu
 
    leads_without_assigned_to = frappe.get_all("Lead",
                        filters={"custom_assign_to": ("in", [None])},
                        fields=["name", "lead_owner", "status"])
 
    for lead in leads_without_assigned_to:
        if lead.lead_owner in user_dict:
            user_dict[lead.lead_owner]["lead"] += 1
            if lead["status"] == "Lost":
                user_dict[lead.lead_owner]["lost"] += 1
            if lead["status"] == "Converted":
                user_dict[lead.lead_owner]["converted"] += 1
            if lead.name in lead_follow_ups_map:
                fu = 0
                if "Open" in lead_follow_ups_map[lead.name]:
                    user_dict[lead.lead_owner]["open_fu"] += lead_follow_ups_map[lead.name]["Open"]
                    fu += lead_follow_ups_map[lead.name]["Open"]
                if "Closed" in lead_follow_ups_map[lead.name]:
                    user_dict[lead.lead_owner]["closed_fu"] += lead_follow_ups_map[lead.name]["Closed"]
                    fu += lead_follow_ups_map[lead.name]["Closed"]
                user_dict[lead.lead_owner]["followup"] += fu
 
    # Calculate Lead Count by subtracting Lead Lost Count from Total Lead Count
    for user_data in user_dict.values():
        user_data["lead_count"] = user_data["lead"] - user_data["lost"]
        
    data = list(user_dict.values())
    
    # Get data for Sandesh
    sandesh_user_data = get_sandesh_user_data()
    data.append(sandesh_user_data)
 
    return data
 
 
def get_sandesh_user_data():
    # Initialize sandesh_user_data dictionary
    sandesh_user_data = {
        "full_name": "",  # Full name of the user
        "user": "sandesh@advancedhealth.in",  # User email address
        "lead": 0,  # Total lead count for the user
        "lost": 0,  # Lead lost count for the user
        "lead_count": 0,  # Lead count (Total Lead Count - Lead Lost Count)
        "followup": 0,  # Total lead follow-up count for the user
        "open_fu": 0,  # Open follow-up count for the user
        "closed_fu": 0,  # Closed follow-up count for the user
        "converted": 0  # Converted lead count for the user
    }
 
    # Fetch user information from the database
    user_data = frappe.get_all("User", filters={"email": "sandesh@advancedhealth.in"}, fields=["full_name"])
    if user_data:
        sandesh_user_data["full_name"] = user_data[0].get("full_name", "")
 
    # Fetch lead-related information for the user from the database
    leads_data = frappe.get_all("Lead", fields=["name", "status"])
    sandesh_user_data["lead"] = len(leads_data)
    sandesh_user_data["lost"] = sum(1 for lead in leads_data if lead.get("status") == "Lost")
    sandesh_user_data["lead_count"] = sandesh_user_data["lead"] - sandesh_user_data["lost"]
    sandesh_user_data["converted"] = sum(1 for lead in leads_data if lead.get("status") == "Converted")
 
    # Fetch all lead follow-up counts for the user from the database
    lead_follow_ups = frappe.get_all("Lead Follow Up", fields=["name", "status"])
    sandesh_user_data["followup"] = len(lead_follow_ups)
    sandesh_user_data["open_fu"] = sum(1 for fu in lead_follow_ups if fu.get("status") == "Open")
    sandesh_user_data["closed_fu"] = sum(1 for fu in lead_follow_ups if fu.get("status") == "Closed")
 
    return sandesh_user_data
 
 
 
# Main function to execute the report
def execute(filters=None):
    # Define report columns with minimum width
    columns = [
        {"label": "Full Name", "fieldname": "full_name", "fieldtype": "Data", "width": 150},
        {"label": "Email", "fieldname": "user", "fieldtype": "Data", "width": 150},
        {"label": "Total Lead Count", "fieldname": "lead", "fieldtype": "Int", "width": 150},
        {"label": "Open Lead Count", "fieldname": "lead_count", "fieldtype": "Int", "width": 150},
        {"label": "Converted Count", "fieldname": "converted", "fieldtype": "Int", "width": 150},
        {"label": "Lead Lost Count", "fieldname": "lost", "fieldtype": "Int", "width": 150},
        {"label": "Lead Follow Up Count", "fieldname": "followup", "fieldtype": "Int", "width": 180},  # Total follow-up count
        {"label": "Open Followed Up Count", "fieldname": "open_fu", "fieldtype": "Int", "width": 180},  # Open follow-up count
        {"label": "Closed Follow Up Count", "fieldname": "closed_fu", "fieldtype": "Int", "width": 180}  # Closed follow-up count
    ]
 
    # Query data for user "sandesh@advancedhealth.in"
    if filters and filters.get("user") == "sandesh@advancedhealth.in":
        sandesh_user_data = get_sandesh_user_data()
        return columns, sandesh_user_data
 
    # For other users or when no specific user is selected, query data as before
    all_users_data = get_all_users_data()
    return columns, all_users_data
