import frappe
import time
from frappe.model.document import Document
from pypika import Order
from frappe.query_builder.functions import Count


class Student(Document):
    a=1

    def before_insert(self):
        frappe.msgprint("before_insert called")

    def before_naming(self):
        frappe.msgprint("before_naming called")

    def autoname(self):
        self.name = f"joker" + str(Student.a)
        Student.a+=1

    def before_validate(self):
        if self.first_name and self.last_name:
            self.full_name = f"{self.first_name} {self.last_name}"

    def validate(self):
        print("this is controller")
        if not self.first_name:
            self.first_name = self.student_name + "MF"

        if self.year and not 1 <= self.year <= 4:
            frappe.throw("Year must be between 1 and 4")

        if self.phone and (not self.phone.isdigit() or len(self.phone) != 10):
            frappe.throw("Phone must contain exactly 10 digits")

    def before_save(self):
        if self.department and self.year:
            self.student_code = f"STU-{self.department}-{self.year}"

    def after_insert(self):
        frappe.msgprint("Student inserted successfully")

    def on_update(self):
        frappe.msgprint("Student updated")

    def on_change(self):
        frappe.logger().info(f"Student changed: {self.name}")

    def before_rename(self, old_name, new_name, merge=False):
        frappe.msgprint(f"Renaming {old_name} to {new_name}")

    def after_rename(self, old_name, new_name, merge=False):
        frappe.msgprint(f"Renamed successfully to {new_name}")

    def on_trash(self):
        courses = frappe.db.count(
            "Student Course",
            {"student": self.name}
        )

        if courses:
            frappe.throw(
                "Cannot delete Student because Course records exist"
            )

    def after_delete(self):
        frappe.msgprint("Student deleted")

    @frappe.whitelist()
    def change(self):
        self.email = "itachi@gmail.com"
        print(frappe.session.user, frappe.get_meta)
        self.save()

    @frappe.whitelist()
    def delete(self):
        frappe.db.delete("Student")
        
    @frappe.whitelist()
    def sql(self):
        data = frappe.db.sql(
            """
            select * from tabStudent;
            """
        )
        Student = frappe.qb.DocType("Student")

        query = frappe.qb.from_(Student).select(Count(Student.name), Student.department).where(Student.department == "CSE").groupby(Student.department)
        result = query.run()        
        
        return result
    @frappe.whitelist()
    def generate_report(self):
        frappe.enqueue(
            "aerele_assignment.aa_practice.doctype.student.student.process_student_report",
            student_name=self.name,
            queue="long",
            timeout=300
        )

        frappe.publish_realtime("realtime_sample")

        return "Report generation started"

import frappe

from frappe.utils.xlsxutils import XLSXMetadata, XLSXStyleBuilder


def execute(filters=None):
    columns = [
        {
            "fieldname": "student_name",
            "label": "Student Name",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "fieldname": "first_name",
            "label": "First Name",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "fieldname": "last_name",
            "label": "Last Name",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "fieldname": "email",
            "label": "Email",
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "fieldname": "phone",
            "label": "Phone",
            "fieldtype": "Data",
            "width": 120,
        },
        {
            "fieldname": "department",
            "label": "Department",
            "fieldtype": "Select",
            "width": 100,
        },
        {
            "fieldname": "year",
            "label": "Year",
            "fieldtype": "Int",
            "width": 80,
        },
        {
            "fieldname": "status",
            "label": "Status",
            "fieldtype": "Select",
            "width": 100,
        },
        {
            "fieldname": "full_name",
            "label": "Full Name",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "fieldname": "admission_date",
            "label": "Admission Date",
            "fieldtype": "Date",
            "width": 120,
        },
        {
            "fieldname": "student_code",
            "label": "Student Code",
            "fieldtype": "Data",
            "width": 120,
        },
    ]

    data = frappe.get_all(
        "Student",
        fields=[
            "student_name",
            "first_name",
            "last_name",
            "email",
            "phone",
            "department",
            "year",
            "status",
            "full_name",
            "admission_date",
            "student_code",
        ],
        order_by="creation desc",
    )

    return columns, data

@frappe.whitelist()
def get_xlsx_styles(metadata: XLSXMetadata) -> dict:
    builder = XLSXStyleBuilder(metadata)

    # --------------------------------------------------
    # 1. Register custom styles
    # --------------------------------------------------

    header_style = builder.register_style(
        {
            "bold": True,
            "align": "center",
            "valign": "vcenter",
            "text_wrap": True,
            "border": 1,
            "border_color": "#000000",
            "bg_color": "#D9EAF7",
            "font_size": 11,
        }
    )

    data_style = builder.register_style(
        {
            "valign": "vcenter",
            "border": 1,
            "border_color": "#D0D0D0",
        }
    )

    center_style = builder.register_style(
        {
            "align": "center",
            "valign": "vcenter",
            "border": 1,
            "border_color": "#D0D0D0",
        }
    )

    date_style = builder.register_style(
        {
            "align": "center",
            "valign": "vcenter",
            "num_format": "yyyy-mm-dd",
            "border": 1,
            "border_color": "#D0D0D0",
        }
    )

    # --------------------------------------------------
    # 2. Header row
    # --------------------------------------------------

    # Row 0 is the report header
    builder.style_row(0, header_style)

    # --------------------------------------------------
    # 3. Data columns
    # --------------------------------------------------

    student_name_col = builder.field_index_map.get("student_name")
    first_name_col = builder.field_index_map.get("first_name")
    last_name_col = builder.field_index_map.get("last_name")
    email_col = builder.field_index_map.get("email")
    phone_col = builder.field_index_map.get("phone")
    department_col = builder.field_index_map.get("department")
    year_col = builder.field_index_map.get("year")
    status_col = builder.field_index_map.get("status")
    full_name_col = builder.field_index_map.get("full_name")
    admission_date_col = builder.field_index_map.get("admission_date")
    student_code_col = builder.field_index_map.get("student_code")

    # Normal data columns
    for col in [
        student_name_col,
        first_name_col,
        last_name_col,
        email_col,
        phone_col,
        full_name_col,
        student_code_col,
    ]:
        if col is not None:
            builder.style_column(col, data_style)

    # Centered columns
    for col in [
        department_col,
        year_col,
        status_col,
    ]:
        if col is not None:
            builder.style_column(col, center_style)

    # Date column
    if admission_date_col is not None:
        builder.style_column(admission_date_col, date_style)

    # --------------------------------------------------
    # 4. Return styles
    # --------------------------------------------------

    return builder.result
        


@frappe.whitelist()
def truncate_student():
    print(frappe.db.get_doc("Student"))




def process_student_report(student_name):

    frappe.logger().info(
        f"Background job started for Student: {student_name}"
    )

    student = frappe.get_doc("Student", student_name)

    courses = frappe.get_all(
        "Student Course",
        filters={
            "student": student.name
        },
        fields=["name", "course_name"]
    )

    for course in courses:

        time.sleep(2)

        frappe.logger().info(
            f"Processing course: {course.course_name}"
        )

    frappe.logger().info(
        f"Report completed for Student: {student.name}"
    )


