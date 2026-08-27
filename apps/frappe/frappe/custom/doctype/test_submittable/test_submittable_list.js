frappe.listview_settings["test_submittable"] = {
    onload(listview) {
        listview.page.add_inner_button("My Button", () => {

            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "test_submittable",
                    filters: {
                        docstatus: 1
                    },
                    fields: [
                        "name",
                        "item",
                        "price"
                    ],
                    limit_page_length: 100
                },
                callback(r) {

                    const documents = r.message || [];

                    let html = "";

                    if (documents.length === 0) {
                        html = "<p>No submitted documents found.</p>";
                    } else {
                        html = `
                            <table class="table table-bordered">
                                <thead>
                                    <tr>
                                        <th>Name</th>
                                        <th>Item</th>
                                        <th>Price</th>
                                    </tr>
                                </thead>
                                <tbody>
                        `;

                        documents.forEach(doc => {
                            html += `
                                <tr>
                                    <td>${doc.name}</td>
                                    <td>${doc.item || ""}</td>
                                    <td>${doc.price || 0}</td>
                                </tr>
                            `;
                        });

                        html += `
                                </tbody>
                            </table>
                        `;
                    }

                    const dialog = new frappe.ui.Dialog({
                        title: "Submitted Documents",
                        fields: [
                            {
                                fieldtype: "HTML",
                                fieldname: "documents"
                            }
                        ]
                    });

                    dialog.fields_dict.documents.$wrapper.html(html);

                    dialog.show();
                }
            });

        });
    }
};