import frappe
from frappe.utils import now

@frappe.whitelist()
def update_test_documents(allow_guest=True):
    test_document = frappe.qb.DocType("Test Doc")
    test_item = frappe.qb.DocType("Test Item")

    results = (
    frappe.qb.from_(test_document)
    .join(test_item)
    .on(test_item.test_doc == test_document.name)
    .select(
        test_document.name,
        test_document.description,
        test_document.status,
        test_item.item_name,
        test_item.quantity,
    )
    .limit(10)
).run(as_dict=True)

    if not results:
        return []

    doc = frappe.get_doc("Test Doc", results[0]["name"])
    doc.description = "Updated using Document API"
    doc.save()

    names = [row["name"] for row in results]

    for name in names:
        frappe.db.set_value(
            "Test Doc",
            name,
            "status",
            "Processed",
        )

    return results


@frappe.whitelist()
def get_recent_todos():
    todos = frappe.get_list(
        "ToDo",
        fields=["name", "description", "owner"],
        order_by="creation desc",
        limit_page_length=5
    )

    records = []

    for todo in todos:
        email = frappe.db.get_value(
            "User",
            todo.owner,
            "email"
        )

        records.append({
            "name": todo.name,
            "description": todo.description,
            "owner_email": email
        })

    return {
        "timestamp": now(),
        "records": records
    }

@frappe.whitelist()
def create_test_doc(task_subject):
    doc = frappe.new_doc("Test Doc")
    doc.description = task_subject
    doc.status = "Pending"
    doc.save()

    return doc.name


# let dialog = new frappe.ui.Dialog({
#     title: "Create Test Doc",
#     fields: [
#         {
#             fieldname: "task_subject",
#             label: "Task Subject",
#             fieldtype: "Data",
#             reqd: 1
#         }
#     ],
#     primary_action_label: "Create Test Doc",

#     primary_action(values) {
#         frappe.call({
#             method: "aerele_assignment.api.create_test_doc",
#             args: {
#                 task_subject: values.task_subject
#             },
#             callback: function (response) {
#                 dialog.hide();

#                 frappe.msgprint({
#                     title: "Success",
#                     message: `Test Doc <b>${response.message}</b> was created successfully.`,
#                     indicator: "green"
#                 });
#             }
#         });
#     }
# });

# dialog.show();