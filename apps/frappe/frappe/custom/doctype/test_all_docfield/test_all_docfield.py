# Copyright (c) 2026, Frappe Technologies and contributors
# For license information, please see license.txt

# import frappe
import math
from frappe.model.document import Document


class testalldocfield(Document):
	a = 1

	def autoname(self):
		self.name = self.sample + self.not_sample + "siuuuu"
