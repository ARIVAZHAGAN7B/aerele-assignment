import time
import frappe
from frappe.utils import now

def test_worker():
    frappe.log_error(
        title="WORKER START",
        message=f"Started at {now()}"
    )

    time.sleep(10)

    frappe.log_error(
        title="WORKER END",
        message=f"Finished at {now()}"
    )