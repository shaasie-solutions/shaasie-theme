from . import __version__ as app_version

app_name        = "customize_erpnext"
app_title       = "Customize ERPNext"
app_publisher   = "Shaasie Solutions"
app_description = "Custom print styles, print formats, and desk themes for ERPNext — Cairo font, RTL support, clean install/uninstall"
app_email       = "support@shaasie.com"
app_license     = "MIT"

# ── Desk assets ───────────────────────────────────────────────────────────────
# Loaded ONLY on the ERPNext desk (/app) — never on website or login pages.
app_include_css = [
    "/assets/customize_erpnext/css/ce_themes.css",
]

app_include_js = [
    "/assets/customize_erpnext/js/theme_switcher.js",
]

# ── Theme override ────────────────────────────────────────────────────────────
# Frappe's original switch_theme only accepts "light", "dark", "automatic".
# Our override extends the allowed list with "ce_blue", "ce_green", "ce_red"
# so Frappe saves and restores the user's CE theme across sessions.
override_whitelisted_methods = {
    "frappe.core.doctype.user.user.switch_theme": "customize_erpnext.overrides.switch_theme.switch_theme",
}

# ── Lifecycle hooks ───────────────────────────────────────────────────────────
after_install   = "customize_erpnext.install.after_install"
after_uninstall = "customize_erpnext.install.after_uninstall"

# ── Fixtures ──────────────────────────────────────────────────────────────────
# HOW TO ADD A NEW PRINT FORMAT:
#   1. Create the Print Format inside ERPNext (desk → Print Format doctype).
#   2. Add its name to the filter list below and to PRINT_FORMATS in install.py.
#   3. Export: bench --site <site> export-fixtures --app customize_erpnext
#   4. Commit the updated fixtures/print_format.json.
#
fixtures = [
    {
        "dt": "Print Style",
        "filters": [["name", "in", ["CE Print Style"]]],
    },
    # ── Uncomment and extend when print formats are added ─────────────────────
    # {
    #     "dt": "Print Format",
    #     "filters": [["name", "in", [
    #         "CE Sales Invoice",
    #         # add more names here …
    #     ]]],
    # },
]
