# Copyright (c) 2026, Frappe Technologies and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class parent_table(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.practice.doctype.child_table.child_table import child_table
		from frappe.types import DF

		child_table: DF.Table[child_table]
		parent_name: DF.Data | None
	# end: auto-generated types

	pass
