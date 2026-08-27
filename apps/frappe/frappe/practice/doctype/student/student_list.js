frappe.ui.form.on("Student", {

    refresh(frm) {

        frm.add_custom_button("Fetch Course", function () {

            frappe.call({
                method: "frappe.practice.doctype.student.student.get_course_by_student",

                args: {
                    student_name: frm.doc.name
                },

                callback: function (r) {

                    const courses = r.message || [];

                    if (courses.length === 0) {
                        frappe.msgprint({
                            title: "Courses",
                            message: "No courses found for this student."
                        });

                        return;
                    }

                    let html = `
                        <div style="
                            display: flex;
                            flex-direction: column;
                            gap: 12px;
                        ">
                    `;

                    courses.forEach(course => {

                        html += `
                            <div style="
                                border: 1px solid #d1d8dd;
                                border-radius: 8px;
                                padding: 15px;
                            ">

                                <h4 style="margin-top: 0;">
                                    ${course.course_name}
                                </h4>

                                <p>
                                    <b>Course ID:</b>
                                    ${course.course_id || "-"}
                                </p>

                                <p>
                                    <b>Course:</b>
                                    ${course.name}
                                </p>

                            </div>
                        `;

                    });

                    html += `</div>`;

                    frappe.msgprint({
                        title: `Courses of ${frm.doc.name}`,
                        message: html,
                        wide: true
                    });

                }
            });

        });

    }

});


rappe.ui.form.on("Student", {

    refresh(frm) {

        frm.add_custom_button("Meta", function () {

            frappe.call({
                method: "frappe.practice.doctype.student.student.get_student_meta",

                callback: function (r) {

                    let html = `
                        <div style="
                            display: flex;
                            flex-direction: column;
                            gap: 12px;
                        ">
                    `;

                    html += <h1>`${r.message}`</h1>

                    html += `</div>`;

                    frappe.msgprint({
                        message: html
                    });

                }
            });

        });

    }

});