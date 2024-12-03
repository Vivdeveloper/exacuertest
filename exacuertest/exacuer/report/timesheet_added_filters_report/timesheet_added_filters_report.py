import frappe
from frappe import _
from frappe.desk.reportview import build_match_conditions

def execute(filters=None):
    if not filters:
        filters = {}

    columns = get_columns()
    conditions = get_conditions(filters)
    data = get_data(conditions, filters)

    total_hours = sum(float(row[2]) for row in data)

    total_hours = "{:.2f}".format(total_hours)

    total_row = ["", _("Total"), total_hours, "", "", "", "", ""]
    data.append(total_row)

    return columns, data

def get_columns():
    return [
        _("Employee") + "::150",
        _("Employee Name") + "::150",
        _("Total Hours") + "::70",
        _("Sales Count") + "::70",
        _("Project") + ":Link/Project:120",
        _("Project Name") + "::150",
        _("Customer") + ":Link/Customer:150",
        _("Custom Type") + "::120"
    ]

def get_data(conditions, filters):
    time_sheet = frappe.db.sql(
        """SELECT 
            `tabTimesheet`.employee, 
            `tabTimesheet`.employee_name,
            SUM(`tabTimesheet Detail`.hours) AS total_hours, 
            `tabTimesheet Detail`.custom_sales_count,  
            `tabTimesheet Detail`.project, 
            `tabProject`.project_name, 
            `tabTimesheet`.customer, 
            `tabTimesheet`.custom_type
        FROM 
            `tabTimesheet Detail`
        JOIN 
            `tabTimesheet` ON `tabTimesheet Detail`.parent = `tabTimesheet`.name
        JOIN 
            `tabProject` ON `tabTimesheet Detail`.project = `tabProject`.name
        JOIN 
            `tabEmployee` ON `tabTimesheet`.employee = `tabEmployee`.name
        WHERE 
            `tabEmployee`.status = 'Active' AND %s
        GROUP BY 
            `tabTimesheet`.employee, 
            `tabTimesheet Detail`.project, 
            `tabProject`.project_name, 
            `tabTimesheet`.customer, 
            `tabTimesheet`.custom_type, 
            `tabTimesheet Detail`.custom_sales_count  
        ORDER BY 
            `tabTimesheet`.employee""" % (conditions),
        filters,
        as_list=1,
    )

    for row in time_sheet:
        row[2] = "{:.2f}".format(row[2])

    return time_sheet

def get_conditions(filters):
    conditions = "`tabTimesheet`.docstatus = 1"
    
    if filters.get("start_date"):
        conditions += " AND `tabTimesheet Detail`.from_time >= %(start_date)s"
    if filters.get("end_date"):
        conditions += " AND `tabTimesheet Detail`.to_time <= %(end_date)s"
    
    if filters.get("employee"):
        conditions += " AND `tabTimesheet`.employee = %(employee)s"
    if filters.get("project"):
        conditions += " AND `tabTimesheet Detail`.project = %(project)s"
    if filters.get("customer"):
        conditions += " AND `tabTimesheet`.customer = %(customer)s"
    if filters.get("custom_type") is not None:
        conditions += " AND `tabTimesheet`.custom_type = %(custom_type)s"
    
    match_conditions = build_match_conditions("Timesheet")
    if match_conditions:
        conditions += " AND %s" % match_conditions

    return conditions or "1=1"
