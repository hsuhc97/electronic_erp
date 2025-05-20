# Copyright (c) 2025, Orient AI and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import (
	cint,
	cstr,
	flt,
	formatdate,
	get_link_to_form,
	getdate,
	now_datetime,
	nowtime,
	strip,
	strip_html,
)

class Item(Document):
	def validate(self):
		if not self.item_name:
			self.item_name = self.item_code
		
		if not strip_html(cstr(self.description)).strip():
			self.description = self.item_name


@frappe.whitelist()
def get_item_attribute(parent, attribute_value=""):
	"""Used for providing auto-completions in child table."""
	if not frappe.has_permission("Item"):
		frappe.throw(_("No Permission"))

	return frappe.get_all(
		"Item Attribute Value",
		fields=["attribute_value"],
		filters={"parent": parent, "attribute_value": ("like", f"%{attribute_value}%")},
	)
