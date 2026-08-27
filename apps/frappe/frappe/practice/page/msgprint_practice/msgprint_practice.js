frappe.pages["msgprint_practice"].on_page_load = function (wrapper) {
    let page = frappe.ui.make_app_page({
        parent: wrapper,
        title: "msgprint Practice",
        single_column: true
    });

    $(page.body).html(`
        <div style="display:flex; flex-direction:column; gap:10px; width:400px">

            <button class="btn btn-primary" id="basic">
                1. Basic
            </button>

            <button class="btn btn-primary" id="title">
                2. Title
            </button>

            <button class="btn btn-primary" id="table">
                3. Table
            </button>

            <button class="btn btn-primary" id="list">
                4. List
            </button>

            <button class="btn btn-primary" id="indicator">
                5. Indicator
            </button>

            <button class="btn btn-primary" id="wide">
                6. Wide
            </button>

            <button class="btn btn-primary" id="minimizable">
                7. Minimizable
            </button>

            <button class="btn btn-danger" id="exception">
                8. Raise Exception
            </button>
			<button class = "btn btn-primary" id="server-action"> click pannu mamey </button>


        </div>
    `);


    $("#basic").click(function () {
        frappe.call({
            method: "frappe.aapi.basic"
        });
    });


    $("#title").click(function () {
        frappe.call({
            method: "frappe.aapi.custom_title"
        });
    });


    $("#table").click(function () {
        frappe.call({
            method: "frappe.aapi.table"
        });
    });


    $("#list").click(function () {
        frappe.call({
            method: "frappe.aapi.list_message"
        });
    });


    $("#indicator").click(function () {
        frappe.call({
            method: "frappe.aapi.indicator"
        });
    });


    $("#wide").click(function () {
        frappe.call({
            method: "frappe.aapi.wide"
        });
    });


    $("#minimizable").click(function () {
        frappe.call({
            method: "frappe.aapi.minimizable"
        });
    });


    $("#exception").click(function () {
        frappe.call({
            method: "frappe.aapi.exception"
        });
    });

	$("#server-action").click(function () {
    frappe.call({
        method: "frappe.aapi.primary_server_action"
    });
});
};