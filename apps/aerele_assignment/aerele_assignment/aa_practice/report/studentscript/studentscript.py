import frappe


def execute(filters=None):
    filters = filters or {}

    columns = get_columns()
    data = get_data(filters)

    return columns, data


def get_columns():
    return [
        {
            "label": "Student Name",
            "fieldname": "student_name",
            "fieldtype": "Data",
            "width": 180,
        },
        {
            "label": "First Name",
            "fieldname": "first_name",
            "fieldtype": "Data",
            "width": 140,
        },
        {
            "label": "Last Name",
            "fieldname": "last_name",
            "fieldtype": "Data",
            "width": 140,
        },
        {
            "label": "Email",
            "fieldname": "email",
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "label": "Phone",
            "fieldname": "phone",
            "fieldtype": "Data",
            "width": 130,
        },
        {
            "label": "Department",
            "fieldname": "department",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "label": "Year",
            "fieldname": "year",
            "fieldtype": "Int",
            "width": 80,
        },
        {
            "label": "Status",
            "fieldname": "status",
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "label": "Full Name",
            "fieldname": "full_name",
            "fieldtype": "Data",
            "width": 180,
        },
        {
            "label": "Admission Date",
            "fieldname": "admission_date",
            "fieldtype": "Date",
            "width": 130,
        },
        {
            "label": "Student Code",
            "fieldname": "student_code",
            "fieldtype": "Data",
            "width": 130,
        },
    ]


def get_data(filters):
    conditions = {}

    if filters.get("department"):
        conditions["department"] = filters.get("department")

    if filters.get("year"):
        conditions["year"] = filters.get("year")

    if filters.get("status"):
        conditions["status"] = filters.get("status")

    data = frappe.get_all(
        "Student",
        filters=conditions,
        fields=[
            "student_name",
            "first_name",
            "last_name",
            "email",
            "phone",
            "department",
            "year",
            "status",
            "full_name",
            "admission_date",
            "student_code",
        ],
        order_by="creation desc",
    )

    return data