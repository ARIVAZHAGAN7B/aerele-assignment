import frappe


@frappe.whitelist()
def basic():
    frappe.msgprint("Hello from server")


@frappe.whitelist()
def custom_title():
    frappe.msgprint(
        "Student saved successfully",
        title="Success"
    )


@frappe.whitelist()
def table():
    data = [
        ["Name", "Department", "Year"],
        ["Arivazhagan", "CSE", 4],
        ["Kumar", "ECE", 3],
        ["Ravi", "AIDS", 2]
    ]

    frappe.msgprint(
        data,
        title="Students",
        as_table=True
    )


@frappe.whitelist()
def list_message():
    data = [
        "Python",
        "Frappe",
        "MariaDB",
        "Redis"
    ]

    frappe.msgprint(
        data,
        title="Technologies",
        as_list=True
    )


@frappe.whitelist()
def indicator():
    frappe.msgprint(
        "Student saved successfully",
        title="Success",
        indicator="green"
    )


@frappe.whitelist()
def wide():
    frappe.msgprint(
        "This is a wide message modal.",
        title="Wide Modal",
        wide=True
    )


@frappe.whitelist()
def minimizable():
    frappe.msgprint(
        "You can minimize this modal.",
        title="Minimizable",
        is_minimizable=True
    )


@frappe.whitelist()
def exception():
    frappe.msgprint(
        "Student is not valid.",
        title="Validation Error",
        raise_exception=True
    )


@frappe.whitelist()
def primary_server_action():
    frappe.msgprint(
        "Do you want to perform the action?",
        title="Server Action",
        primary_action={
            "label": "Proceed",
            "server_action": "frappe.aapi.server_action_clicked"
        }
    )


@frappe.whitelist()
def server_action_clicked():
    frappe.msgprint(
        "Server action was executed!",
        title="Success",
        indicator="green"
    )