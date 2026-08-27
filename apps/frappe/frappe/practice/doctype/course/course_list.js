frappe.listview_settings["Course"] = {
    onload(listview) {

        listview.page.add_inner_button("try utils", () => {
            frappe.msgprint(
                String(frappe.utils.add(10, 40))
            )
        })

        listview.page.add_inner_button("open modal", () => {
            let d = new frappe.ui.Dialog({
                title: 'Enter details',
                fields: [
                    {
                        label: 'First Name',
                        fieldname: 'first_name',
                        fieldtype: 'Data'
                    },
                    {
                        label: 'Last Name',
                        fieldname: 'last_name',
                        fieldtype: 'Data'
                    },
                    {
                        label: 'Age',
                        fieldname: 'age',
                        fieldtype: 'Int'
                    }
                ],
                size: 'small',
                primary_action_label: 'Submit',
                primary_action(values) {
                    console.log(values);
                    d.hide();
                }
            });

            d.show();

        })


        listview.page.add_inner_button("Trigger", () => {
            frappe.confirm("confirm pannuriyae mamey",
                () => {
                    frappe.prompt('name sollura jokeru', ({ value }) => {
                        console.log(value);
                    })
                },
                () => {
                    frappe.warn("no kudutha breakup da unaku", "breakup aanalum paravilya?",
                        () => {
                            console.log("kadaisi varaikum single thanda nee")
                            frappe.show_alert({ message: __("single thanda nee"), indicator: 'green' }, 1)
                        },
                        'Continue',
                        true
                    )
                }
            )
        })

        listview.page.add_inner_button("Course", () => {
            frappe.call({
                method: "frappe.practice.doctype.course.course.sample"
            });
        })
    }
}