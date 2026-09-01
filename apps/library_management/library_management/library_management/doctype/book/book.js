frappe.ui.form.on("Book", {
	refresh(frm) {
		// available_copies is system-managed via Book Rental submit/cancel/return
		frm.set_df_property("available_copies", "read_only", 1);
	},

	total_copies(frm) {
		if (frm.is_new() && frm.doc.total_copies) {
			frm.set_value("available_copies", frm.doc.total_copies);
		}
	},
});
