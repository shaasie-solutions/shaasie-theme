"""
Override for frappe.core.doctype.user.user.switch_theme

Frappe's original function only allows "dark", "light", and "automatic".
We extend it to also accept our three custom theme names so Frappe
saves and restores the user's CE theme correctly across sessions.

Registered in hooks.py → override_whitelisted_methods.
"""

import frappe


@frappe.whitelist()
def switch_theme(theme: str) -> None:
    """Save the chosen desk theme to the current user's record."""
    allowed_themes = {
        # Frappe built-in themes — keep them working
        "light",
        "dark",
        "automatic",
        # Customization app themes
        "ce_blue",
        "ce_green",
        "ce_red",
    }

    if theme in allowed_themes:
        frappe.db.set_value("User", frappe.session.user, "desk_theme", theme)
