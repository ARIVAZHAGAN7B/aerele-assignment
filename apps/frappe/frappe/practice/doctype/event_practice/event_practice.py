# Copyright (c) 2026, Frappe Technologies and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class EventPractice(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		amended_from: DF.Link | None
		amount: DF.Currency
		description: DF.SmallText | None
		email: DF.Data | None
		event_date: DF.Data | None
		items: DF.Link | None
		phone: DF.Data | None
		status: DF.Literal["Draft", "Confirmed", "Cancelled"]
		student: DF.Link | None
		title: DF.Data | None
	# end: auto-generated types

	pass
