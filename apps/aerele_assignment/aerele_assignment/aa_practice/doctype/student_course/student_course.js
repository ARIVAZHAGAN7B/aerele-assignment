frappe.ui.form.on("Student Course", {

    refresh(frm) {
        console.log("Student Course refreshed");
    },

    credits(frm) {
        if (frm.doc.credits && frm.doc.credits <= 0) {
            frappe.msgprint("Credits must be greater than 0");
        }
    }

});