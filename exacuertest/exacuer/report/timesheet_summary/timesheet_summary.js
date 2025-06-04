// Copyright (c) 2025, eg and contributors
// For license information, please see license.txt

frappe.query_reports["Timesheet Summary"] = {
	"filters": [
		{
			"fieldname": "start_date",
			"label": __("Start Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_days(frappe.datetime.now_date(), -30)
		},
		{
			"fieldname": "end_date",
			"label": __("End Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.now_date()
		},
		{
			"fieldname": "project",
			"label": __("Project"),
			"fieldtype": "Link",
			"options": "Project"
		},
		
		{
			"fieldname": "employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee"
		},
			
	]
};
