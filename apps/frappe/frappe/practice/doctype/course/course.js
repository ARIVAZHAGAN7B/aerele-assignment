frappe.realtime.on("sample", () => {
    console.log("Function 1");
});

frappe.realtime.on("sample", () => {
    console.log("Function 2");
});