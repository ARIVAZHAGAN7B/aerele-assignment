import frappe
from frappe import _
from frappe.model.document import Document


class Library(Document):

    def validate(self):
        self.validate_status()

    def validate_status(self):
        if self.status not in ["Active", "Inactive"]:
            frappe.throw(_("Invalid library status."))