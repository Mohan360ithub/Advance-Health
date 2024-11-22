import frappe
from frappe.utils import getdate, nowdate
from datetime import datetime, timedelta


def execute(filters=None):
    filters = frappe._dict(filters or {})
    columns = get_columns()
    data = get_data(filters)
    return columns, data, None

def get_columns():
    columns = [
        {"label": "Source", "fieldname": "source", "fieldtype": "Data", "width": 200},
        {"label": "Total Lead Count", "fieldname": "total_lead_count", "fieldtype": "Int", "width": 150},
        {"label": "Converted Lead Count", "fieldname": "converted_lead_count", "fieldtype": "Int", "width": 150},
        {"label": "Interested Lead Count", "fieldname": "interested_lead_count", "fieldtype": "Int", "width": 150},
        {"label": "Overdue Lead Count", "fieldname": "overdue_lead_count", "fieldtype": "Int", "width": 150},
        {"label": "Lost Lead Count", "fieldname": "lost_lead_count", "fieldtype": "Int", "width": 150},
    ]
    return columns

def get_data(filters):
    # Get the duration and custom_created_at (date range) filters
    duration = filters.get('duration', 'All The Time')
    date_range = filters.get('custom_created_at', None)
    # print('date_rangeeeeeeeeeeeeeeeeeeeeeeee',date_range)
    where_conditions = []
    assign_to = filters.get('custom_assign_to', None)
    if assign_to:
        where_conditions.append(f"custom_assign_to IN ({', '.join(['%s' % frappe.db.escape(x) for x in assign_to])})")

    if duration != "All The Time":
        if duration == "Today":
            where_conditions.append(f"custom_created_on = '{nowdate()}'")
        elif duration == "Weekly":
            start_of_week = get_start_of_week()
            where_conditions.append(f"custom_created_on >= '{start_of_week}'")
        elif duration == "Monthly":
            first_day_of_month = get_first_day_of_month()
            where_conditions.append(f"custom_created_on >= '{first_day_of_month}'")
        elif duration == "Qtrly":
            quarter_start_date = get_quarter_start_date()
            where_conditions.append(f"custom_created_on >= '{quarter_start_date}'")
        elif duration == "Date Range Wise" and date_range:
            if isinstance(date_range, list) and len(date_range) == 2:
                start_date, end_date = date_range
                where_conditions.append(f"custom_created_on BETWEEN '{start_date}' AND '{end_date}'")
    
    # Add any additional filters here
    filters_condition = " AND ".join(where_conditions) if where_conditions else "1=1"

    # SQL query to fetch lead counts by source
    leads_data = frappe.db.sql(f"""
        SELECT source, status, COUNT(name) as count
        FROM `tabLead`
        WHERE {filters_condition}
        GROUP BY source, status
    """, as_dict=True)

    # Aggregate lead counts by source and status
    source_counts = {}
    for row in leads_data:
        source = row.source or "Other"
        status = row.status
        if source not in source_counts:
            source_counts[source] = {
                "total_lead_count": 0,
                "converted_lead_count": 0,
                "interested_lead_count": 0,
                "overdue_lead_count": 0,
                "lost_lead_count": 0,
            }
        source_counts[source]["total_lead_count"] += row.count
        if status == "Converted":
            source_counts[source]["converted_lead_count"] += row.count
        elif status == "Interested":
            source_counts[source]["interested_lead_count"] += row.count
        elif status == "Lost":
            source_counts[source]["lost_lead_count"] += row.count
        elif status == "Overdue":
            source_counts[source]["overdue_lead_count"] += row.count

    # Prepare the final data for the report
    data = []
    for source, counts in source_counts.items():
        row = {
            "source": source,
            **counts,
        }
        data.append(row)

    return data

# Helper functions for start of the week, month, and quarter
def get_start_of_week():
    today = datetime.today()
    start_of_week = today - timedelta(days=today.weekday())
    return start_of_week.date()

def get_first_day_of_month():
    today = datetime.today()
    return datetime(today.year, today.month, 1).date()

def get_quarter_start_date():
    today = datetime.today()
    month = today.month
    if month in [1, 2, 3]:
        return datetime(today.year, 1, 1).date()
    elif month in [4, 5, 6]:
        return datetime(today.year, 4, 1).date()
    elif month in [7, 8, 9]:
        return datetime(today.year, 7, 1).date()
    else:
        return datetime(today.year, 10, 1).date()
