import frappe
from frappe import _
from frappe.desk.reportview import build_match_conditions

def execute(filters=None):
	if not filters:
		filters = {}
	elif filters.get("start_date") or filters.get("end_date"):
		filters["from_time"] = "00:00:00"
		filters["to_time"] = "24:00:00"

	columns = get_columns()
	conditions = get_conditions(filters)
	data = get_data(conditions, filters)

	return columns, data

def get_columns():
	return [
		_("Employee") + "::150",
		_("Employee Name") + "::150",
		_("Total Hours") + "::70",
		_("Project") + ":Link/Project:120",
		_("Customer") + ":Link/Customer:150"
	]

def get_data(conditions, filters):
	time_sheet = frappe.db.sql(
		"""select `tabTimesheet`.employee, `tabTimesheet`.employee_name,
		SUM(`tabTimesheet Detail`.hours) as total_hours, `tabTimesheet Detail`.project,
		`tabTimesheet`.customer
		from `tabTimesheet Detail`
		join `tabTimesheet` on `tabTimesheet Detail`.parent = `tabTimesheet`.name
		where %s
		group by `tabTimesheet`.employee, `tabTimesheet Detail`.project, `tabTimesheet`.customer
		order by `tabTimesheet`.employee""" % (conditions),
		filters,
		as_list=1,
	)

	return time_sheet

def get_conditions(filters):
	conditions = "`tabTimesheet`.docstatus = 1"
	if filters.get("start_date"):
		conditions += " and `tabTimesheet Detail`.from_time >= %(start_date)s"
	if filters.get("end_date"):
		conditions += " and `tabTimesheet Detail`.to_time <= %(end_date)s"
	if filters.get("employee"):
		conditions += " and `tabTimesheet`.employee = %(employee)s"
	if filters.get("project"):
		conditions += " and `tabTimesheet Detail`.project = %(project)s"
	if filters.get("customer"):
		conditions += " and `tabTimesheet`.customer = %(customer)s"

	match_conditions = build_match_conditions("Timesheet")
	if match_conditions:
		conditions += " and %s" % match_conditions

	return conditions
