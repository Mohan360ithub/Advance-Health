import frappe
from frappe import _

def execute(filters=None):
    # Set default value for from_date filter to today's date if not provided
    if not filters:
        filters = {"from_date": [frappe.utils.nowdate(), frappe.utils.nowdate()]}

    columns = [
        _("Full Name") + ":Link/User:150",
        _("Email") + ":Data:150",
        _("Lead Follow Up Count") + ":Int:150",
    ]

    data = []

    if "from_date" in filters:
        start_date, end_date = filters["from_date"]
        filters["start_date"] = frappe.utils.get_datetime(start_date)
        filters["end_date"] = frappe.utils.get_datetime(end_date)
        del filters["from_date"]
    else:
        frappe.throw("Please select valid date range.")

    assigned_to, owner = get_lead_follow_up_count(filters)
    lead_follow_up_count_dict = {}

    for i in assigned_to:
        key = (i["full_name"], i["email"])
        lead_follow_up_count_dict[key] = lead_follow_up_count_dict.get(key, 0) + i["lead_follow_up_count"]

    for i in owner:
        key = (i["full_name"], i["email"])
        lead_follow_up_count_dict[key] = lead_follow_up_count_dict.get(key, 0) + i["lead_follow_up_count"]

    for key, value in lead_follow_up_count_dict.items():
        data.append([key[0], key[1], value])

    return columns, data

def get_lead_follow_up_count(filters):
    query_assigned_to = """
        SELECT
            u.full_name,
            u.email,
            COUNT(lfu.name) as lead_follow_up_count
        FROM
            `tabLead Follow Up` lfu
        LEFT JOIN
            `tabUser` u ON lfu.assigned_to_test = u.name
        WHERE
            lfu.date BETWEEN %(start_date)s AND %(end_date)s
            AND lfu.assigned_to_test IS NOT NULL
        GROUP BY
            u.full_name, u.email
    """

    query_owner = """
        SELECT
            u.full_name,
            u.email,
            COUNT(lfu.name) as lead_follow_up_count
        FROM
            `tabLead Follow Up` lfu
        LEFT JOIN
            `tabUser` u ON lfu.owner_test = u.name
        WHERE
            lfu.date BETWEEN %(start_date)s AND %(end_date)s
            AND lfu.assigned_to_test IS NULL
        GROUP BY
            u.full_name, u.email
    """

    assigned_to = frappe.db.sql(query_assigned_to, filters, as_dict=True)
    owner = frappe.db.sql(query_owner, filters, as_dict=True)

    return assigned_to, owner
