frappe.ui.form.on("test_submittable", {
	refresh(frm) {
        frm.add_custom_button("Say Hello", () => {
            frappe.msgprint("Hello!");
        });
	},
});