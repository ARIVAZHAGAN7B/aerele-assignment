import frappe
from frappe.model.document import Document


class single(Document):


	from typing import TYPE_CHECKING

	@frappe.whitelist()
	def get_value(self):
		return self.value
	
	if TYPE_CHECKING:
		from frappe.types import DF

		singular: DF.Data | None
	# end: auto-generated types

	pass
