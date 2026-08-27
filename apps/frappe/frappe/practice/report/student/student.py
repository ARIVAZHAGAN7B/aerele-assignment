def execute(filters=None):
    columns = [
        {
            "label": "Student Name",
            "fieldname": "student_name",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": "Roll Number",
            "fieldname": "roll_number",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": "Department",
            "fieldname": "department",
            "fieldtype": "Data",
            "width": 120
        }
    ]

    data = [
        {
            "student_name": "Arun",
            "roll_number": "101",
            "department": "CSE"
        },
        {
            "student_name": "Kumar",
            "roll_number": "102",
            "department": "ECE"
        },
        {
            "student_name": "Ravi",
            "roll_number": "103",
            "department": "AIML"
        }
    ]

    return columns, data