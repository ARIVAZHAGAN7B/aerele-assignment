frappe.ui.form.on("v-d-f", {

    f_name(frm) {
        update_full_name(frm);
    },

    l_name(frm) {
        update_full_name(frm);
    }

});


function update_full_name(frm) {
    const first = frm.doc.f_name || "";
    const last = frm.doc.l_name || "";

    frm.set_value(
        "full_name",
        `${first} ${last}`.trim()
    );
}