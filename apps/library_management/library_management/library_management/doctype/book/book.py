import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class Book(Document):

	def validate(self):
		self.validate_library()
		self.validate_total_copies()
		self.initialize_or_update_copies()
		self.update_status()

	def validate_library(self):

		if not self.library:
			frappe.throw(_("Library is required."))

		library_status = frappe.db.get_value(
			"Library",
			self.library,
			"status"
		)

		if not library_status:
			frappe.throw(
				_("Selected library does not exist.")
			)

		if library_status != "Active":
			frappe.throw(
				_("Cannot add a book to an inactive library.")
			)

	def validate_total_copies(self):

		if flt(self.total_copies) < 0:
			frappe.throw(
				_("Total copies cannot be negative.")
			)

	def initialize_or_update_copies(self):

		# New Book
		if self.is_new():
			self.available_copies = self.total_copies
			return

		old_total = frappe.db.get_value(
			"Book",
			self.name,
			"total_copies"
		)

		old_available = frappe.db.get_value(
			"Book",
			self.name,
			"available_copies"
		)

		if old_total is None:
			return

		old_total = flt(old_total)
		old_available = flt(old_available)
		new_total = flt(self.total_copies)

		difference = new_total - old_total

		new_available = old_available + difference

		if new_available < 0:
			frappe.throw(
				_(
					"Total copies cannot be reduced below "
					"the number of currently rented copies."
				)
			)

		if new_available > new_total:
			frappe.throw(
				_("Available copies cannot exceed total copies.")
			)

		self.available_copies = new_available

	def update_status(self):

		if self.available_copies > 0:
			self.status = "Available"
		else:
			self.status = "Unavailable"