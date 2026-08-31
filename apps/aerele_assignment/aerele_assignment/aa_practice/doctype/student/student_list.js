frappe.listview_settings["Student"] = {
    onload(listview) {
        listview.page.add_inner_button("fetch", () => {
            frappe.call({
                method: "aerele_assignment.aa_practice.doctype.student.student.truncate_student",
                callback: function (r) {
                    console.log(r);
                }
            });
        })

        listview.page.add_inner_button("exl", () => {
            frappe.call({
                method:"aerele_assignment.aa_practice.doctype.student.student.get_xlsx_styles"
            })
        })
    }
}
