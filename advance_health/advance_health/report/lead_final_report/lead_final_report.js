frappe.query_reports["Lead Final Report"] = {
    "filters": [
        {
            "fieldname": "duration",
            "label": __("Duration"),
            "fieldtype": "Select",
            "options": "\nAll The Time\nToday\nWeekly\nMonthly\nQtrly\nDate Range Wise",  // Added "Date Range Wise"
            "default": "All The Time",
            "on_change": function(query_report) {
                let duration = frappe.query_report.get_filter_value('duration');
                
                // Toggle visibility of date range filter based on the duration selection
                frappe.query_report.toggle_filter_display('custom_created_at', duration !== 'Date Range Wise');
                
                // Handle the filter logic based on the selected duration
                if (duration === 'All The Time') {
                    // Reset filter for custom_created_at
                    frappe.query_report.set_filter_value('custom_created_at', null);
                } else if (duration === 'Today') {
                    let today = frappe.datetime.get_today();
                    frappe.query_report.set_filter_value('custom_created_at', [today, today]);  // Set today's date
                } else if (duration === 'Weekly') {
                    let today = new Date();
                    let start_of_week = new Date(today.setDate(today.getDate() - today.getDay()));  // Start of the current week (Sunday)
                    let end_of_week = new Date(today.setDate(today.getDate() + 6));  // Saturday
                    frappe.query_report.set_filter_value('custom_created_at', [start_of_week, end_of_week]);
                } else if (duration === 'Monthly') {
                    let first_of_month = frappe.datetime.month_start(frappe.datetime.get_today());
                    let last_of_month = frappe.datetime.month_end(frappe.datetime.get_today());
                    frappe.query_report.set_filter_value('custom_created_at', [first_of_month, last_of_month]);
                } else if (duration === 'Qtrly') {
                    let quarter_start = get_quarter_start_date();
                    let quarter_end = frappe.datetime.add_days(quarter_start, 90);  // Approx 3 months
                    frappe.query_report.set_filter_value('custom_created_at', [quarter_start, quarter_end]);
                }
                
                // Refresh the report after setting the date range filter
                query_report.refresh();
            }
        },
        {
            "fieldname": "custom_created_at",
            "label": __("Created At"),
            "fieldtype": "DateRange",
            "hidden": 1,  // Initially hidden, will be shown when Date Range Wise is selected
            "on_change": function(query_report) {
                // Trigger the refresh when date range is changed
                query_report.refresh();
            }
        },
        {
			"fieldname": "custom_assign_to",
			"label": __("Assigned To"),
			"fieldtype": "MultiSelectList",
			"fieldtype": "MultiSelectList",
            "options": "User",
            "get_data": function (txt) {
                return frappe.db.get_link_options("User", txt, {
                    // Add any filters you need, for example:
                    // company: frappe.query_report.get_filter_value("company"),
                });
            },
		}
		
		
		
    ]
};

// Function to get the start date of the current quarter
function get_quarter_start_date() {
    let today = new Date();
    let month = today.getMonth() + 1; // Get current month (1-12)
    let quarter_start_month = Math.floor((month - 1) / 3) * 3 + 1; // Start of the current quarter
    return frappe.datetime.add_days(new Date(today.getFullYear(), quarter_start_month - 1, 1), 0);
}
