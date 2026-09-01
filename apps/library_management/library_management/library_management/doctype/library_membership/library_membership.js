frappe.ui.form.on("Library Membership", {
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
