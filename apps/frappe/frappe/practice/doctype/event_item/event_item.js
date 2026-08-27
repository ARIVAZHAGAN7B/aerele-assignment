frappe.ui.form.on("Event Item", {
    item_name(frm, cdt, cdn) {
        console.log("Item name changed");

        let row = locals[cdt][cdn];

        console.log(row.item_name);
    },

    qty(frm, cdt, cdn) {
        console.log("Quantity changed");

        let row = locals[cdt][cdn];

        if (row.qty < 1) {
            frappe.model.set_value(cdt, cdn, "qty", 1);
        }
    },

    rate(frm, cdt, cdn) {
        console.log("Rate changed");

        let row = locals[cdt][cdn];

        console.log("Rate:", row.rate);
    }
});