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


frappe.ui.form.on("Book", {
	refresh(frm) {

		if (
			!frm.is_new() &&
			frm.doc.available_copies > 0 &&
			frm.doc.status === "Available"
		) {

			frm.add_custom_button(
				__("Rent Book"),
				() => {

					frappe.confirm(
						__("Do you want to rent this book?"),
						() => {

							frm.call({
								method: "rent_book",
								doc: frm.doc,
								freeze: true,
								freeze_message: __("Renting book...")
							}).then((r) => {

								if (r.message) {

									frappe.show_alert({
										message: __(
											"Book rented successfully. Rental: {0}",
											[
												r.message.rental
											]
										),
										indicator: "green"
									});

									frm.reload_doc();
								}
							});
						}
					);
				}
			);
		}
	}
});