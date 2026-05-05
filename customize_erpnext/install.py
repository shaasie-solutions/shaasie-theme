"""
Lifecycle hooks for Customize ERPNext.

after_install   — runs once when: bench install-app <site> customize_erpnext
after_uninstall — runs once when: bench remove-app  <site> customize_erpnext

Both functions are idempotent — safe to call multiple times.

HOW TO REGISTER A NEW PRINT FORMAT FOR CLEAN UNINSTALL:
  Add its name to PRINT_FORMATS below so after_uninstall deletes it cleanly.
"""

import frappe

# ── Records owned by this app ─────────────────────────────────────────────────
PRINT_STYLES = ["CE Print Style"]

# Add the name of every Print Format you export here.
PRINT_FORMATS: list[str] = []

# Custom Fields created by this app — deleted on uninstall.
# Name format in Frappe: "{DocType}-{fieldname}"
CUSTOM_FIELDS = [
    "System Settings-ce_theme_section",
    "System Settings-ce_desk_theme",
]


def after_install():
    """
    Sync fixtures immediately after install so records are available
    without needing a separate `bench migrate`.
    """
    _sync_fixtures()
    frappe.db.commit()
    frappe.msgprint(
        msg=(
            "Customize ERPNext installed successfully.<br><br>"
            "Print Style <b>CE Print Style</b> is available in the print dialog.<br>"
            "Desk Theme selector added to <b>Settings → System Settings → Customize ERPNext</b>.<br><br>"
            "Choose Blue, Green, or Red — save and reload the page to apply."
        ),
        title="Customize ERPNext",
        indicator="green",
    )


def after_uninstall():
    """
    Remove every record created by this app — no orphaned data left behind.
    """
    _delete_records("Print Format", PRINT_FORMATS)
    _delete_records("Print Style", PRINT_STYLES)
    _delete_custom_fields(CUSTOM_FIELDS)
    frappe.db.commit()


# ── Helpers ───────────────────────────────────────────────────────────────────

def _sync_fixtures():
    """Import this app's fixture JSON files into the database."""
    try:
        from frappe.utils.fixtures import sync_fixtures
        sync_fixtures(app="customize_erpnext")
    except Exception:
        frappe.log_error(frappe.get_traceback(), "customize_erpnext: fixture sync skipped")


def _delete_records(doctype: str, names: list[str]) -> None:
    """Safely delete a list of records if they still exist."""
    for name in names:
        if frappe.db.exists(doctype, name):
            try:
                frappe.delete_doc(doctype, name, force=True, ignore_missing=True)
            except Exception:
                frappe.log_error(
                    frappe.get_traceback(),
                    f"customize_erpnext: could not delete {doctype} '{name}'",
                )


def _delete_custom_fields(names: list[str]) -> None:
    """Safely delete Custom Field records created by this app."""
    for name in names:
        if frappe.db.exists("Custom Field", name):
            try:
                frappe.delete_doc("Custom Field", name, force=True, ignore_missing=True)
            except Exception:
                frappe.log_error(
                    frappe.get_traceback(),
                    f"customize_erpnext: could not delete Custom Field '{name}'",
                )
