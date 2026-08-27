frappe.ui.form.on("Event Practice", {
    setup(frm) {
        console.log("1. setup");
        frappe.msgprint("setup");
        frm.set_value("description", "new-event")
    },

    before_load(frm) {
        console.log("2. before_load");
    },

    onload(frm) {
        console.log("3. onload");
    },

    refresh(frm) {
        console.log("4. refresh");

        if (!frm.is_new()) {
            frm.add_custom_button("Test Button", () => {
                frappe.msgprint("Button clicked");
            });
        }

        frm.add_custom_button("Attach File", () => {
            if (frm.is_dirty()) {
                frappe.show_alert(
                    "Please save form before attaching a file"
                );
                return;
            }

            // continue with attachment logic
        });
    },

    onload_post_render(frm) {
        console.log("5. onload_post_render");
    },

    validate(frm) {
        console.log("6. validate");

        if (frm.doc.amount < 0) {
            frappe.throw("Amount cannot be negative");
        }
    },

    before_save(frm) {
        console.log("7. before_save");

        frm.doc.description =
            frm.doc.description || "Created from Event Practice";
    },

    after_save(frm) {
        console.log("8. after_save");

        frappe.show_alert({
            message: "Document saved",
            indicator: "green"
        });
    },

    before_submit(frm) {
        console.log("9. before_submit");

        if (!frm.doc.event_date) {
            frappe.throw("Event Date is required before submitting");
        }
    },

    on_submit(frm) {
        console.log("10. on_submit");

        frappe.msgprint("Event has been submitted");
    },

    before_cancel(frm) {
        console.log("11. before_cancel");

        if (frm.doc.status === "Confirmed") {
            frappe.throw("Confirmed events cannot be cancelled");
        }
    },

    after_cancel(frm) {
        console.log("12. after_cancel");

        frappe.msgprint("Event cancelled");
    },

    before_discard(frm) {
        console.log("13. before_discard");

        console.log("About to discard:", frm.doc.name);
    },

    after_discard(frm) {
        console.log("14. after_discard");

        frappe.msgprint("Event discarded");
    },

    timeline_refresh(frm) {
        console.log("15. timeline_refresh");
    },

    title(frm) {
        console.log("16. title changed");

        if (frm.doc.title) {
            frm.set_value(
                "description",
                "Event: " + frm.doc.title
            );
        }
    },

    amount(frm) {
        console.log("17. amount changed");

        if (frm.doc.amount > 10000) {
            frappe.show_alert({
                message: "High-value event",
                indicator: "orange"
            });
        }
    },

    get_email_recipient_filters(frm, field) {
        console.log("18. get_email_recipient_filters", field);

        return {
            status: "Active"
        };
    },

    get_email_recipients(frm, field) {
        console.log("19. get_email_recipients", field);

        if (frm.doc.email) {
            return [frm.doc.email];
        }

        return [];
    }

    
});