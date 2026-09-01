frappe.ui.form.on("Library Membership", {
	refresh(frm) {
		frm.add_custom_button("extend", () => {
			frappe.prompt({
				"label": "how many days",
				"fieldname":"days",
				"fieldtype":"Int"
			}, (values) => {
				frappe.call({
					"method":"library_management.library_management.doctype.library_membership.library_membership.extend_validation",
					args:{
						name:frm.doc.name,
						days:values.days,
					}
				})
			})
		})

	},
	setup(frm) {
		frm.set_query("library", () => ({
			filters: { status: "Active" },
		}));
	},

	user(frm) {
		if (frm.doc.user && frm.is_new()) {
			frm.set_value("start_date", frappe.datetime.now_datetime());
		}
	},
});
