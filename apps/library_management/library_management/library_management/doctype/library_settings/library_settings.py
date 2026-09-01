import frappe
from frappe import _
from frappe.model.document import Document


class LibrarySettings(Document):

    def validate(self):
        self.validate_rental_days()
        self.validate_fine_per_day()
        self.validate_maximum_books()

    def validate_rental_days(self):
        if self.rental_days <= 0:
            frappe.throw(_("Rental Days must be greater than zero."))

    def validate_fine_per_day(self):
        if self.fine_per_day < 0:
            frappe.throw(_("Fine Per Day cannot be negative."))

    def validate_maximum_books(self):
        if self.maximum_books <= 0:
            frappe.throw(_("Maximum Books must be greater than zero."))