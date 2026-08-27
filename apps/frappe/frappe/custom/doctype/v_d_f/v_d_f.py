# Copyright (c) 2026, Frappe Technologies and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class vdf(Document):
	@property
	def full_name(self):
		return (self.f_name or " ") + " " + (self.l_name or " ")
