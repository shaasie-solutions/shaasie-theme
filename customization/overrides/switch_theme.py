"""
Override for frappe.core.doctype.user.user.switch_theme

Root cause of the "theme resets on refresh" bug:
  Frappe's ThemeSwitcher calls toggle_theme("ce_blue") which internally
  sends toTitle("ce_blue") = "Ce_blue" to this Python function.
  The old code checked for exact lowercase "ce_blue" so "Ce_blue" never
  matched — nothing was saved — and on refresh Frappe rendered the old
  theme from the DB.

Fix:
  Normalize the incoming theme name to lowercase + underscores before
  the allow-list check. This handles all forms Frappe may send:
    "Ce_blue"  →  "ce_blue"
    "CE_BLUE"  →  "ce_blue"
    "Light"    →  "light"
    "Dark"     →  "dark"

Registered in hooks.py → override_whitelisted_methods.
"""

import frappe


@frappe.whitelist()
def switch_theme(theme: str) -> None:
    """Save the chosen desk theme to the current user's record."""
    # Normalize: handle "Ce_blue", "CE_BLUE", "Light", "Dark", etc.
    normalized = theme.strip().lower().replace(" ", "_")

    allowed_themes = {
        # Frappe built-in themes
        "light",
        "dark",
        "automatic",
        # CE custom themes
        "ce_blue",
        "ce_green",
        "ce_red",
    }

    if normalized in allowed_themes:
        frappe.db.set_value("User", frappe.session.user, "desk_theme", normalized)
