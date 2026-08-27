from frappe.model.document import Document


class test_submittable(Document):

	def autoname(self):
		self.name = f"STU-{self.item}"

	def before_save(self):
		self.price = self.price * 2

	def before_submit(self):
		pass


	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		amended_from: DF.Link | None
		item: DF.Data | None
		price: DF.Int
	# end: auto-generated types

	pass
