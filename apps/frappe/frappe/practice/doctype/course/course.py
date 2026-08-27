# Copyright (c) 2026, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Course(Document):



	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		course_id: DF.Data | None
		course_name: DF.Data | None
		student: DF.Link | None
	# end: auto-generated types

	pass

@frappe.whitelist()
def sample():
	print("sample is called")
	frappe.publish_realtime("sample")