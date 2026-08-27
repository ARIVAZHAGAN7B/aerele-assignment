# Copyright (c) 2026, Frappe Technologies and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Add(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	def validate(self):
		self.sum = self.num1 + self.num2
		

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		num1: DF.Int
		num2: DF.Int
		sum: DF.Int
	# end: auto-generated types

	pass
