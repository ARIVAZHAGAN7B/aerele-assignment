frappe.listview_settings["Order"] = {
    onload(listview) {
        listview.page.add_inner_button("Show Items", () => {
            show_order_items(listview);
        });

        listview.page.add_inner_button("Route Get", () => {
            const route = frappe.get_route();

            frappe.msgprint(route.join(" → "));
        });

        listview.page.add_inner_button("Route Set", () => {
            const route = frappe.set_route("List", "Student", "Report");
        });

        listview.page.add_inner_button("Show Format", () => {
            let b = 78;

            let formatted = frappe.format(b, {
                fieldtype: "Currency",
                options: "INR"
            });

            frappe.msgprint(formatted);
        });

        listview.page.add_inner_button("Provide Test", () => {
            frappe.provide("frappe.utils");

            frappe.utils.add = function (a, b) {
                return a + b;
            };

            frappe.msgprint(
                String(frappe.utils.add(10, 20))
            );
        });


    }
};




async function show_order_items(listview) {
    const orders = listview.data;

    if (!orders || orders.length === 0) {
        frappe.msgprint("No orders found.");
        return;
    }

    const order_names = orders.map(order => order.name);

    const response = await frappe.call({
        method: "frappe.custom.doctype.order.order.get_order_items",
        args: {
            order_names: order_names
        }
    });

    const items = response.message || [];

    if (items.length === 0) {
        frappe.msgprint("No child items found.");
        return;
    }

    let html = `
        <table class="table table-bordered">
            <thead>
                <tr>
                    <th>Order</th>
                    <th>Customer</th>
                    <th>Date</th>
                    <th>Item</th>
                    <th>Quantity</th>
                    <th>Rate</th>
                    <th>Amount</th>
                </tr>
            </thead>
            <tbody>
    `;

    for (const row of items) {
        html += `
            <tr>
                <td>${frappe.utils.escape_html(row.parent)}</td>
                <td>${frappe.utils.escape_html(row.customername || "")}</td>
                <td>${frappe.utils.escape_html(row.transactiondate || "")}</td>
                <td>${frappe.utils.escape_html(row.item || "")}</td>
                <td>${row.quantity || 0}</td>
                <td>${row.rate || 0}</td>
                <td>${row.amount || 0}</td>
            </tr>
        `;
    }

    html += `
            </tbody>
        </table>
    `;

    const dialog = new frappe.ui.Dialog({
        title: "Order Items",
        size: "extra-large",
        fields: [
            {
                fieldtype: "HTML",
                fieldname: "items_html"
            }
        ]
    });

    dialog.fields_dict.items_html.$wrapper.html(html);

    dialog.show();
}