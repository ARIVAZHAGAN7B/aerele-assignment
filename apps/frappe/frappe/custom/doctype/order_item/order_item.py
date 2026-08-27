# Copyright (c) 2026, Frappe Technologies and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class OrderItem(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		amount: DF.Currency
		item: DF.Data | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		quantity: DF.Int
		rate: DF.Currency
	# end: auto-generated types

	pass
