frappe.ui.form.on("Book Rental", {


    onload(frm) {
        frappe.call({
            method: "library_management.library_management.doctype.book_rental.book_rental.currentUser",
        }).then((r) => {
            const data = r.message;

            frm.set_value("user", data.user);
            frm.set_value("membership", data.membership);
            frm.set_value("library", data.library);
        });
    },

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