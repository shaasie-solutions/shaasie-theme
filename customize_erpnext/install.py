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
# after_uninstall will delete them all cleanly.
PRINT_FORMATS: list[str] = []


def after_install():
    """
    Sync fixtures immediately after install so records are available
    without needing a separate `bench migrate`.
    """
    _sync_fixtures()
    frappe.db.commit()
    frappe.msgprint(
        msg=(
            "Customize ERPNext installed successfully.<br>"
            "Print Style <b>CE Print Style</b> is now available in the print dialog.<br>"
            "Add your Print Formats via <code>bench export-fixtures</code> when ready."
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
