import frappe
from frappe.model.document import Document


class Student(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        department: DF.Data | None
        roll_number: DF.Data | None
        student_name: DF.Data | None
        year: DF.Literal["1", "2", "3", "4"]
    # end: auto-generated types

    pass


@frappe.whitelist()
def get_course_by_student(student_name):

    courses = frappe.get_all(
        "Course",
        filters={
            "student": student_name
        },
        fields=[
            "name",
            "course_id",
            "course_name"
        ]
    )

    return courses



@frappe.whitelist()
def get_student_meta(self):
    return frappe.get_meta('Student')
