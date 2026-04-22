import frappe


def after_uninstall():
    """Remove the print style created by this app on uninstall."""
    if frappe.db.exists("Print Style", "Shaasie Style"):
        frappe.delete_doc("Print Style", "Shaasie Style", force=True)
        frappe.db.commit()
