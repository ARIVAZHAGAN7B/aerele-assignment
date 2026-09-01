# Copyright (c) 2026, library and Contributors
# See license.txt

import frappe
from frappe.tests import IntegrationTestCase
from frappe.utils import add_days, today


# On IntegrationTestCase, the doctype test records and all
# link-field test record dependencies are recursively loaded
# Use these module variables to add/remove to/from that list
EXTRA_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]
IGNORE_TEST_RECORD_DEPENDENCIES = []  # eg. ["User"]


class IntegrationTestBookRental(IntegrationTestCase):
	"""
	Integration tests for BookRental.
	Use this class for testing interactions between multiple components.
	"""

	def setUp(self):
		self.settings = frappe.get_single("Library Settings")
		self.settings.rental_days = 7
		self.settings.fine_per_day = 20
		self.settings.maximum_books = 1
		self.settings.save(ignore_permissions=True)

		suffix = frappe.generate_hash(length=8)
		self.library = frappe.new_doc("Library")
		self.library.library_name = f"Rental Test Library {suffix}"
		self.library.status = "Active"
		self.library.insert(ignore_permissions=True)

		self.book = frappe.new_doc("Book")
		self.book.title = f"Rental Test Book {suffix}"
		self.book.library = self.library.name
		self.book.total_copies = 3
		self.book.available_copies = 3
		self.book.insert(ignore_permissions=True)

		self.user = frappe.new_doc("User")
		self.user.email = f"rental-{frappe.generate_hash(length=8)}@example.com"
		self.user.first_name = "Rental"
		self.user.insert(ignore_permissions=True)

		self.membership = frappe.new_doc("Library Membership")
		self.membership.user = self.user.name
		self.membership.library = self.library.name
		self.membership.start_date = today()
		self.membership.end_date = add_days(today(), 30)
		self.membership.status = "Active"
		self.membership.insert(ignore_permissions=True)

	def test_rental_submit_reduces_available_copies(self):
		rental = frappe.new_doc("Book Rental")
		rental.user = self.user.name
		rental.membership = self.membership.name
		rental.library = self.library.name
		rental.book = self.book.name
		rental.rental_date = today()
		rental.insert(ignore_permissions=True)
		rental.submit()

		book = frappe.get_doc("Book", self.book.name)
		self.assertEqual(book.available_copies, 2)

	def test_return_book_does_not_calculate_fine_immediately(self):
		rental = frappe.new_doc("Book Rental")
		rental.user = self.user.name
		rental.membership = self.membership.name
		rental.library = self.library.name
		rental.book = self.book.name
		rental.rental_date = add_days(today(), -20)
		rental.insert(ignore_permissions=True)
		rental.submit()

		rental.return_book()

		self.assertEqual(rental.status, "Returned")
		self.assertEqual(rental.fine_amount, 0)

		book = frappe.get_doc("Book", self.book.name)
		self.assertEqual(book.available_copies, 3)
