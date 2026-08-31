frappe.ui.form.on("Student Fee", {

    refresh(frm) {
        console.log("Student Fee refreshed");
    },

    amount(frm) {
        calculate_balance(frm);
    },

    paid_amount(frm) {
        calculate_balance(frm);
    }

});

function calculate_balance(frm) {
    let amount = frm.doc.amount || 0;
    let paid = frm.doc.paid_amount || 0;

    frm.set_value("balance", amount - paid);
}