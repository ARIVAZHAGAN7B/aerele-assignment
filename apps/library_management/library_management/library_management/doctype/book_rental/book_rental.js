frappe.ui.form.on("Book Rental", {
    refresh(frm) {

        if (
            !frm.is_new() &&
            ["Rented", "Overdue"].includes(frm.doc.status)
        ) {
            frm.add_custom_button("Return Book", () => {

                frm.call({
                    method: "return_book",
                    doc: frm.doc,
                    freeze: true,
                    freeze_message: __("Returning book...")
                }).then(() => {

                    frm.reload_doc();

                    frappe.show_alert({
                        message: __("Book returned successfully"),
                        indicator: "green"
                    });

                });
            });
        }
    }
});