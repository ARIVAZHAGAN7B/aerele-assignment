# Copyright (c) 2026, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Order(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.custom.doctype.order_item.order_item import OrderItem
        from frappe.types import DF

        customername: DF.Data | None
        iterm: DF.Table[OrderItem]
        transactiondate: DF.Date | None
    # end: auto-generated types

    pass


@frappe.whitelist()
def get_order_items(order_names):
    if isinstance(order_names, str):
        order_names = frappe.parse_json(order_names)

    if not order_names:
        return []

    items = frappe.db.sql(
        """
        SELECT
            oi.parent,
            o.customername,
            o.transactiondate,
            oi.item,
            oi.quantity,
            oi.rate,
            oi.amount
        FROM `tabOrder Item` oi
        INNER JOIN `tabOrder` o
            ON o.name = oi.parent
        WHERE
            oi.parent IN %(orders)s
            AND oi.parenttype = 'Order'
            AND oi.parentfield = 'iterm'
        ORDER BY
            o.creation DESC,
            oi.idx ASC
        """,
        {
            "orders": order_names
        },
        as_dict=True
    )

    return items