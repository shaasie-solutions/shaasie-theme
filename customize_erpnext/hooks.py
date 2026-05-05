from . import __version__ as app_version

app_name        = "customize_erpnext"
app_title       = "Customize ERPNext"
app_publisher   = "Shaasie Solutions"
app_description = "Custom print styles, print formats, and desk themes for ERPNext — Cairo font, RTL support, clean install/uninstall"
app_email       = "support@shaasie.com"
app_license     = "MIT"

# ── Desk assets ───────────────────────────────────────────────────────────────
# app_include_css / app_include_js run ONLY on the ERPNext desk (/app).
# They never affect website pages, login, or portal.
#
# Google Fonts is loaded here (always, for all themes).
# The actual theme CSS (Blue / Green / Red) is injected by theme_loader.js
# based on the value saved in System Settings → CE Desk Theme.
app_include_css = [
    "https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700&display=swap",
]

app_include_js = [
    "/assets/customize_erpnext/js/theme_loader.js",
]

# ── Lifecycle hooks ───────────────────────────────────────────────────────────
after_install   = "customize_erpnext.install.after_install"
after_uninstall = "customize_erpnext.install.after_uninstall"

# ── Boot session ──────────────────────────────────────────────────────────────
# Adds ce_desk_theme to frappe.boot so theme_loader.js can read it
# without an extra API call on every page load.
boot_session = "customize_erpnext.boot.boot_session"

# ── Fixtures ──────────────────────────────────────────────────────────────────
# Fixtures are imported automatically on `bench migrate` and during after_install.
# Filters must reference only records owned by this app — never user data.
#
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
    {
        "dt": "Custom Field",
        "filters": [
            ["dt", "=", "System Settings"],
            ["fieldname", "in", ["ce_theme_section", "ce_desk_theme"]],
        ],
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
