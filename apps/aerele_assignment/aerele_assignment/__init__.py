__version__ = "0.0.1"

import frappe

def custom_func():
    return "Hello"

frappe.custom_func = custom_func