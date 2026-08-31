frappe.ui.form.on("Student", {
    refresh(frm) {
        console.log("Student form refreshed");
    },

    first_name(frm) {
        console.log("first name triggered")
        update_full_name(frm);
    },

    last_name(frm) {
        update_full_name(frm);
    }
});


frappe.ui.form.on("Student", {
    refresh(frm) {
        frm.add_custom_button("Change", () => {
            frm.call("change").then(r => {
            });
        });

        frm.add_custom_button("delete dept", () => {
            frm.call("delete")
        })

        frm.add_custom_button("sql", () => {
            frm.call("sql").then(r => {
                console.log(r);
            })
        })
    }
});



function update_full_name(frm) {
    let first = frm.doc.first_name || "";
    let last = frm.doc.last_name || "";

    frm.set_value("full_name", `${first} ${last}`.trim());
}


frappe.ui.form.on("Student", {
    refresh(frm) {
        frm.add_custom_button("Generate Report", () => {

            frm.call("generate_report").then(r => {
                frappe.msgprint(r.message);
            });
        });
    }
});


frappe.realtime.on("realtime_sample", () => {
    frappe.msgprint("realtime trigerred");
})

frappe.ui.form.on("Student", {
    refresh(frm) {
        frm.add_custom_button("Show Details", () => {

            let html = frappe.render_template(
                "student_modal",
                {
                    first_name: frm.doc.first_name,
                    last_name: frm.doc.last_name,
                    student_name: frm.doc.sname,
                    department: frm.doc.department,
                    phone: frm.doc.phone
                }
            );

            let dialog = new frappe.ui.Dialog({
                title: "Student Details",
                fields: [
                    {
                        fieldtype: "HTML",
                        fieldname: "student_details"
                    }
                ]
            });

            dialog.fields_dict.student_details.$wrapper.html(html);

            dialog.show();
        });
    }
});