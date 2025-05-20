# Copyright (c) 2025, Orient AI and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class TokenGroup(Document):
	def before_save(self):
		if self.original_value:
			tokens = [token.strip() for token in self.original_value.split() if token.strip()]
			if tokens:
				self.first_token = tokens[0]
			self.token_number = len(tokens)
			self.original_value = " ".join(tokens)
			if (self.replacement is None):
				self.replacement = self.original_value

	pass


