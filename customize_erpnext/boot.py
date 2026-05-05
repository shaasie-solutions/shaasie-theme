"""
Boot session hook for Customize ERPNext.

Frappe calls this function once per user session (on login / page refresh).
We add `ce_desk_theme` to `frappe.boot` so theme_loader.js can read it
on the client side without an extra API call.
"""

import frappe


def boot_session(bootinfo):
    """Pass the active desk theme to the browser via frappe.boot."""
    try:
        theme = frappe.db.get_single_value("System Settings", "ce_desk_theme") or "Blue"
        bootinfo.ce_desk_theme = theme.lower()
    except Exception:
        # If the custom field does not exist yet (e.g. before migrate),
        # fall back to Blue silently.
        bootinfo.ce_desk_theme = "blue"
