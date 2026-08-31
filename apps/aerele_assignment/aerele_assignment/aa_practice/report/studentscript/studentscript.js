frappe.query_reports["Student Report"] = {
    filters: [
        {
            fieldname: "department",
            label: __("Department"),
            fieldtype: "Select",
            options: [
                "",
                "CSE",
                "ECE",
                "EEE",
                "AIDS"
            ]
        },

        {
            fieldname: "year",
            label: __("Year"),
            fieldtype: "Int"
        },

        {
            fieldname: "status",
            label: __("Status"),
            fieldtype: "Select",
            options: [
                "",
                "Active",
                "Inactive"
            ]
        }
    ]
};