import frappe
from frappe.model.document import Document


class StudentFee(Document):

    def before_insert(self):
        frappe.msgprint("Fee: before_insert")

    def before_naming(self):
        frappe.msgprint("Fee: before_naming")

    def autoname(self):
        self.name = f"FEE-{frappe.generate_hash(length=6).upper()}"

    def before_validate(self):
        self.balance = (self.amount or 0) - (self.paid_amount or 0)

        if self.balance <= 0:
            self.payment_status = "Paid"
        elif self.paid_amount:
            self.payment_status = "Partial"
        else:
            self.payment_status = "Unpaid"

    def validate(self):
        if not self.student:
            frappe.throw("Student is required")

        if not self.amount or self.amount <= 0:
            frappe.throw("Amount must be greater than 0")

        if self.paid_amount and self.paid_amount > self.amount:
            frappe.throw("Paid Amount cannot be greater than Amount")

    def before_save(self):
        frappe.msgprint("Fee: before_save")

    def after_insert(self):
        frappe.msgprint("Fee inserted successfully")

    def on_update(self):
        frappe.msgprint("Fee updated")

    def before_submit(self):
        if self.payment_status != "Paid":
            frappe.throw(
                "Fee must be fully paid before submission"
            )

        frappe.msgprint("Fee: before_submit")

    def on_submit(self):
        frappe.msgprint(
            f"Fee {self.name} submitted successfully"
        )

    def before_cancel(self):
        frappe.msgprint("Fee: before_cancel")

    def on_cancel(self):
        frappe.msgprint(
            f"Fee {self.name} cancelled"
        )

    def before_update_after_submit(self):
        frappe.msgprint(
            "Fee: before_update_after_submit"
        )

    def on_update_after_submit(self):
        frappe.msgprint(
            "Fee: on_update_after_submit"
        )

    def on_change(self):
        frappe.logger().info(
            f"Student Fee changed: {self.name}"
        )

    def before_rename(self, old_name, new_name, merge=False):
        frappe.msgprint(
            f"Fee renaming: {old_name} → {new_name}"
        )

    def after_rename(self, old_name, new_name, merge=False):
        frappe.msgprint(
            f"Fee renamed to {new_name}"
        )

    def on_trash(self):
        frappe.msgprint(
            f"Deleting Fee: {self.name}"
        )

    def after_delete(self):
        frappe.msgprint(
            "Fee deleted successfully"
        )