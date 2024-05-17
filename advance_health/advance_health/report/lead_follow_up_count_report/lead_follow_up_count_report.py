import frappe
from frappe import _

def execute(filters=None):
    # Set default value for from_date filter to today's date if not provided
    if not filters:
        filters = {"from_date": [frappe.utils.nowdate(), frappe.utils.nowdate()]}
 
    columns = [
        _("Closed By(Full Name)") + ":Link/User:150",
        _("Closed By(Email)") + ":Data:150",
        _("Closed Lead Follow Up Count") + ":Int:150",
        _("Created By(Full Name)") + ":Link/User:150",
        _("Created By(Email)") + ":Data:150",
        _("New Lead Follow Up Count") + ":Int:150",
    ]
 
    data = []
 
    if "from_date" in filters:
        start_date, end_date = filters["from_date"]
        filters["start_date"] = frappe.utils.get_datetime(start_date)
        filters["end_date"] = frappe.utils.get_datetime(end_date)
        del filters["from_date"]
    else:
        frappe.throw("Please select valid date range.")
 
    assigned_to_closed = get_lead_follow_up_count(filters, field="custom_closed_date_time", user_field="custom_closed_by_user_id")
    assigned_to_created = get_lead_follow_up_count(filters, field="custom_created_on", user_field="custom_created_byuser_id")
    
    closed_lead_follow_up_count_dict = {}
    created_lead_follow_up_count_dict = {}
 
    for i in assigned_to_closed:
        key = (i["full_name"], i["email"])
        closed_lead_follow_up_count_dict[key] = closed_lead_follow_up_count_dict.get(key, 0) + i["lead_follow_up_count"]
 
    for i in assigned_to_created:
        key = (i["full_name"], i["email"])
        created_lead_follow_up_count_dict[key] = created_lead_follow_up_count_dict.get(key, 0) + i["lead_follow_up_count"]
 
    for key in set(closed_lead_follow_up_count_dict) | set(created_lead_follow_up_count_dict):
        closed_count = closed_lead_follow_up_count_dict.get(key, 0)
        created_count = created_lead_follow_up_count_dict.get(key, 0)
        data.append([key[0], key[1], closed_count, key[0], key[1], created_count])
 
    return columns, data
 
def get_lead_follow_up_count(filters, field, user_field):
    query_assigned_to = f"""
        SELECT
            u.full_name,
            u.email,
            COUNT(lfu.name) as lead_follow_up_count
        FROM
            `tabLead Follow Up` lfu
        LEFT JOIN
            `tabUser` u ON lfu.{user_field} = u.name
        WHERE
            DATE(lfu.{field}) BETWEEN %(start_date)s AND %(end_date)s
            AND lfu.{user_field} IS NOT NULL
        GROUP BY
            u.full_name, u.email
    """
 
    print("Query:", query_assigned_to)
    print("Filters:", filters)
 
    assigned_to = frappe.db.sql(query_assigned_to, filters, as_dict=True)
    print("Assigned to:", assigned_to)
 
    return assigned_to

