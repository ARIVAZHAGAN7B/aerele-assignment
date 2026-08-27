frappe.ui.form.on("Student", {
    refresh(frm) {
        frm.add_custom_button("Create Contact", () => {

            let dialog = new frappe.ui.Dialog({
                title: "Enter First Name",

                fields: [
                    {
                        label: "First Name",
                        fieldname: "first_name",
                        fieldtype: "Data"
                    }
                ],

                primary_action_label: "Create Contact",

                primary_action(values) {
                    // Get the entered first name
                    let first_name = values.first_name;

                    // Close the dialog
                    dialog.hide();

                    // Pass the value to the new Contact form
                    frappe.route_options = {
                        first_name: first_name
                    };

                    // Open a new Contact
                    frappe.new_doc("Contact");
                }
            });

            // Show the dialog
            dialog.show();
        });
    }
});