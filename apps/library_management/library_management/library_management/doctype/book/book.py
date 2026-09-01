import frappe
from frappe import _
from frappe.model.document import Document


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

		if self.total_copies < 0:
			frappe.throw(
				_("Total copies cannot be negative.")
			)

	def initialize_or_update_copies(self):

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

		difference = self.total_copies - old_total

		new_available = old_available + difference

		if new_available < 0:
			frappe.throw(
				_(
					"Total copies cannot be reduced below "
					"the number of currently rented copies."
				)
			)

		if new_available > self.total_copies:
			frappe.throw(
				_("Available copies cannot exceed total copies.")
			)

		self.available_copies = new_available

	def update_status(self):

		if self.available_copies > 0:
			self.status = "Available"
		else:
			self.status = "Unavailable"

	@frappe.whitelist()
	def rent_book(self):

		user = frappe.session.user

		if user == "Guest":
			frappe.throw(
				_("You must be logged in to rent a book.")
			)

		# Lock the Book row
		book = frappe.db.get_value(
			"Book",
			self.name,
			[
				"name",
				"library",
				"available_copies",
				"status"
			],
			for_update=True,
			as_dict=True
		)

		if not book:
			frappe.throw(_("Book does not exist."))

		# Check availability
		if book.available_copies < 1:
			frappe.throw(
				_("No available copies of {0}.").format(
					self.name
				)
			)

		# Find active membership of logged-in user
		membership = frappe.db.get_value(
			"Library Membership",
			{
				"user": user,
				"library": book.library,
				"status": "Active"
			},
			[
				"name",
				"start_date",
				"end_date"
			],
			as_dict=True
		)

		if not membership:
			frappe.throw(
				_(
					"You do not have an active membership "
					"for {0}."
				).format(book.library)
			)

		# Check membership dates
		today = frappe.utils.getdate()

		if (
			membership.start_date
			and today < frappe.utils.getdate(
				membership.start_date
			)
		):
			frappe.throw(
				_("Your membership has not started yet.")
			)

		if (
			membership.end_date
			and today > frappe.utils.getdate(
				membership.end_date
			)
		):
			frappe.throw(
				_("Your membership has expired.")
			)

		# Check maximum books
		settings = frappe.get_cached_doc(
			"Library Settings"
		)

		if settings.maximum_books:

			active_rentals = frappe.db.count(
				"Book Rental",
				{
					"user": user,
					"status": ["in", ["Rented", "Overdue"]]
				}
			)

			if active_rentals >= settings.maximum_books:
				frappe.throw(
					_(
						"You have reached the maximum limit "
						"of {0} rented books."
					).format(
						settings.maximum_books
					)
				)

		# Create rental
		rental = frappe.get_doc({
			"doctype": "Book Rental",
			"user": user,
			"membership": membership.name,
			"library": book.library,
			"book": book.name,
			"status": "Rented"
		})

		rental.insert(
			ignore_permissions=True
		)

		return {
			"rental": rental.name,
			"book": book.name
		}