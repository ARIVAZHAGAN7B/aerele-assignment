import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import now_datetime, get_datetime, add_to_date, add_days


class LibraryMembership(Document):

    def validate(self):
        self.validate_user()
        self.validate_library()
        self.validate_dates()
        self.validate_duplicate_membership()
        self.update_status()

    def validate_user(self):

        if not self.user:
            frappe.throw(_("User is required."))

        if not frappe.db.exists("User", self.user):
            frappe.throw(_("Selected user does not exist."))

    def validate_library(self):

        if not self.library:
            frappe.throw(_("Library is required."))

        if not frappe.db.exists("Library", self.library):
            frappe.throw(_("Selected library does not exist."))

    def validate_dates(self):

        if self.start_date and self.end_date:

            if get_datetime(self.start_date) > get_datetime(self.end_date):
                frappe.throw(
                    _("Start Date cannot be after End Date.")
                )

    def validate_duplicate_membership(self):

        existing = frappe.db.exists(
            "Library Membership",
            {
                "user": self.user,
                "library": self.library,
                "name": ["!=", self.name]
            }
        )

        if existing:
            frappe.throw(
                _("This user already has a membership for this library.")
            )

    def update_status(self):

        if self.status == "Cancelled":
            return

        now = now_datetime()

        if self.start_date and get_datetime(self.start_date) > now:
            self.status = "Active"
            return

        if self.end_date and get_datetime(self.end_date) < now:
            self.status = "Expired"
            return

        self.status = "Active"
    
@frappe.whitelist()
def extend_validation(name, days:int):
    doc = frappe.get_doc("Library Membership", name)
    doc.end_date = add_days(doc.end_date, days)
    print(frappe.custom_func())
    doc.save()