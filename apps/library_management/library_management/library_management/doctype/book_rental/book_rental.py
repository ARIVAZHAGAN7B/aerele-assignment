import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import (
	getdate,
	get_datetime,
	now_datetime,
	add_days,
	flt,
	date_diff,
)


class BookRental(Document):

	def validate(self):
		self.fetch_library_from_book()

		if self.is_new():
			self.validate_membership()
			self.validate_book_availability()
			self.validate_max_books()
			self.set_rental_period()

	def after_insert(self):
		# New rental consumes one available copy
		self.update_book_copies(-1)

	def fetch_library_from_book(self):
		if not self.book:
			frappe.throw(_("Book is required."))

		self.library = frappe.db.get_value(
			"Book",
			self.book,
			"library"
		)

		if not self.library:
			frappe.throw(
				_("Book {0} does not belong to any library.").format(
					self.book
				)
			)

	def validate_membership(self):
		if not self.membership:
			frappe.throw(_("Library Membership is required."))

		if not self.user:
			frappe.throw(_("User is required."))

		membership = frappe.get_doc(
			"Library Membership",
			self.membership
		)

		# Membership belongs to the selected user
		if membership.user != self.user:
			frappe.throw(
				_("Membership {0} does not belong to User {1}.").format(
					self.membership,
					self.user
				)
			)

		# Membership belongs to the same library as the book
		if membership.library != self.library:
			frappe.throw(
				_(
					"Membership {0} belongs to {1}, but this book "
					"belongs to {2}."
				).format(
					self.membership,
					membership.library,
					self.library
				)
			)

		# Membership must be active
		if membership.status != "Active":
			frappe.throw(
				_("Membership {0} is not Active.").format(
					self.membership
				)
			)

		today = getdate()

		# Membership has not started
		if (
			membership.start_date
			and today < getdate(membership.start_date)
		):
			frappe.throw(
				_("Membership {0} has not started yet.").format(
					self.membership
				)
			)

		# Membership has expired
		if (
			membership.end_date
			and today > getdate(membership.end_date)
		):
			frappe.throw(
				_("Membership {0} has expired.").format(
					self.membership
				)
			)

	def validate_book_availability(self):
		if not self.book:
			frappe.throw(_("Book is required."))

		available_copies = frappe.db.get_value(
			"Book",
			self.book,
			"available_copies",
			for_update=True
		)

		if available_copies is None:
			frappe.throw(
				_("Book {0} does not exist.").format(
					self.book
				)
			)

		if flt(available_copies) < 1:
			frappe.throw(
				_("No available copies of {0}.").format(
					self.book
				)
			)

	def validate_max_books(self):
		settings = frappe.get_cached_doc(
			"Library Settings"
		)

		if not settings.maximum_books:
			return

		active_rentals = frappe.db.count(
			"Book Rental",
			{
				"user": self.user,
				"status": ["in", ["Rented", "Overdue"]],
			}
		)

		if active_rentals >= settings.maximum_books:
			frappe.throw(
				_(
					"User {0} has already reached the maximum "
					"of {1} rented books."
				).format(
					self.user,
					settings.maximum_books
				)
			)

	def set_rental_period(self):
		settings = frappe.get_cached_doc(
			"Library Settings"
		)

		self.rental_date = (
			self.rental_date
			or now_datetime()
		)

		rental_days = settings.rental_days or 14

		self.due_date = (
			self.due_date
			or add_days(
				self.rental_date,
				rental_days
			)
		)

		self.status = "Rented"

	def update_book_copies(self, delta):
		"""
		Update available copies of the Book.

		delta:
			-1 = book rented
			+1 = book returned
		"""

		if not self.book:
			frappe.throw(_("Book is required."))

		# Lock the Book row to prevent concurrent updates
		book_data = frappe.db.get_value(
			"Book",
			self.book,
			["available_copies", "total_copies"],
			for_update=True,
			as_dict=True
		)

		if not book_data:
			frappe.throw(
				_("Book {0} does not exist.").format(
					self.book
				)
			)

		available_copies = flt(
			book_data.available_copies
		)

		total_copies = flt(
			book_data.total_copies
		)

		new_available = available_copies + delta

		if new_available < 0:
			frappe.throw(
				_("Available copies cannot be negative.")
			)

		if new_available > total_copies:
			frappe.throw(
				_("Available copies cannot exceed total copies.")
			)

		status = (
			"Available"
			if new_available > 0
			else "Unavailable"
		)

		frappe.db.set_value(
			"Book",
			self.book,
			{
				"available_copies": new_available,
				"status": status
			},
			update_modified=False
		)

	def calculate_fine(self, return_date):
		if not self.due_date:
			return 0

		return_date = get_datetime(return_date)
		due_date = get_datetime(self.due_date)

		# Returned before/on due date
		if return_date <= due_date:
			return 0

		settings = frappe.get_cached_doc(
			"Library Settings"
		)

		overdue_days = date_diff(
			return_date,
			self.due_date
		)

		return (
			overdue_days
			* flt(settings.fine_per_day)
		)

	@frappe.whitelist()
	def return_book(self):

		if self.status not in ["Rented", "Overdue"]:
			frappe.throw(
				_(
					"Only rented or overdue books "
					"can be returned."
				)
			)

		return_date = now_datetime()

		fine_amount = self.calculate_fine(
			return_date
		)

		# Increase available book count
		self.update_book_copies(1)

		# Update rental
		self.return_date = return_date
		self.fine_amount = fine_amount
		self.status = "Returned"

		self.save(
			ignore_permissions=True
		)

		self.reload()

		return {
			"status": self.status,
			"return_date": self.return_date,
			"fine_amount": self.fine_amount,
		}

def get_permission_query_conditions(user):

	if not user:
		user = frappe.session.user

	return f"`tabBook Rental`.`user` = {frappe.db.escape(user)}"