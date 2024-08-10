// Copyright (c) 2024, eg and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Timesheet added filters Report"] = {
	"filters": [
		{
			"fieldname": "project",
			"label": __("Project"),
			"fieldtype": "Link",
			"options": "Project"
		},
		{
			"fieldname": "custom_type",
			"label": __("Custom Type"),
			"fieldtype": "Select",
			"options": [
				{ "label": __("All"), "value": "" }, 
				{ "label": __("For Client"), "value": "For Client" },
				{ "label": __("For Office Use"), "value": "For Office Use" }
			]
		},
		{
			"fieldname": "employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee"
		},
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
			"fieldname": "customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer"
		},
		
	]
};
