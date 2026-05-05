"""
Lifecycle hooks for Customization.

after_install   — runs once when: bench install-app <site> customization
after_uninstall — runs once when: bench remove-app  <site> customization

Both functions are idempotent — safe to call multiple times.

HOW TO REGISTER A NEW PRINT FORMAT FOR CLEAN UNINSTALL:
  Add its name to PRINT_FORMATS below so after_uninstall deletes it cleanly.
"""

import os
import shutil

import frappe

# ── Records owned by this app ─────────────────────────────────────────────────
PRINT_STYLES = ["CE Print Style"]

# Add the name of every Print Format you export here.
PRINT_FORMATS: list[str] = []


def after_install():
    """
    Publish static assets, sync fixtures, and show a success message.
    Running bench build --app customization is NOT required.
    """
    _publish_assets()
    _sync_fixtures()
    frappe.db.commit()
    frappe.msgprint(
        msg=(
            "Customization installed successfully.<br><br>"
            "Print Style <b>CE Print Style</b> is available in the print dialog.<br>"
            "Desk Themes <b>CE Blue</b>, <b>CE Green</b>, <b>CE Red</b> are now in "
            "the avatar menu → same place as Light and Dark."
        ),
        title="Customization",
        indicator="green",
    )


def after_uninstall():
    """
    Remove every record and asset created by this app — no orphaned data left behind.
    """
    _delete_records("Print Format", PRINT_FORMATS)
    _delete_records("Print Style", PRINT_STYLES)
    _remove_assets()
    frappe.db.commit()


# ── Helpers ───────────────────────────────────────────────────────────────────

def _publish_assets():
    """
    Copy public/js and public/css from the app source into sites/assets/
    so the browser can load them without running bench build.
    """
    try:
        src = os.path.join(frappe.get_app_path("customization"), "public")
        dst = os.path.join(frappe.local.sites_path, "assets", "customization")
        if os.path.exists(src):
            os.makedirs(dst, exist_ok=True)
            shutil.copytree(src, dst, dirs_exist_ok=True)
    except Exception:
        frappe.log_error(frappe.get_traceback(), "customization: asset publish skipped")


def _remove_assets():
    """Remove the published assets folder on uninstall."""
    try:
        dst = os.path.join(frappe.local.sites_path, "assets", "customization")
        if os.path.exists(dst):
            shutil.rmtree(dst)
    except Exception:
        frappe.log_error(frappe.get_traceback(), "customization: asset removal skipped")


def _sync_fixtures():
    """Import this app's fixture JSON files into the database."""
    try:
        from frappe.utils.fixtures import sync_fixtures
        sync_fixtures(app="customization")
    except Exception:
        frappe.log_error(frappe.get_traceback(), "customization: fixture sync skipped")


def _delete_records(doctype: str, names: list[str]) -> None:
    """Safely delete a list of records if they still exist."""
    for name in names:
        if frappe.db.exists(doctype, name):
            try:
                frappe.delete_doc(doctype, name, force=True, ignore_missing=True)
            except Exception:
                frappe.log_error(
                    frappe.get_traceback(),
                    f"customization: could not delete {doctype} '{name}'",
                )
