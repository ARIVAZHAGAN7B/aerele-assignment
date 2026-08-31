import frappe
from frappe.model.document import Document


class StudentCourse(Document):

    def before_insert(self):
        frappe.msgprint("Course: before_insert")

    def before_naming(self):
        frappe.msgprint("Course: before_naming")

    def autoname(self):
        self.name = f"COURSE-{frappe.generate_hash(length=6).upper()}"

    def before_validate(self):
        if not self.status:
            self.status = "Draft"

    def validate(self):
        if not self.student:
            frappe.throw("Student is required")

        if not self.course_name:
            frappe.throw("Course Name is required")

        if self.credits and self.credits <= 0:
            frappe.throw("Credits must be greater than 0")

    def before_save(self):
        frappe.msgprint("Course: before_save")

    def after_insert(self):
        frappe.msgprint("Course inserted successfully")

    def on_update(self):
        frappe.msgprint("Course updated")

    def on_change(self):
        frappe.logger().info(
            f"Student Course changed: {self.name}"
        )

    def before_rename(self, old_name, new_name, merge=False):
        frappe.msgprint(
            f"Course renaming: {old_name} → {new_name}"
        )

    def after_rename(self, old_name, new_name, merge=False):
        frappe.msgprint(
            f"Course renamed to {new_name}"
        )

    def on_trash(self):
        frappe.msgprint(
            f"Deleting Course: {self.name}"
        )

    def after_delete(self):
        frappe.msgprint(
            "Course deleted successfully"
        )