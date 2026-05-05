from . import __version__ as app_version

app_name        = "customize_erpnext"
app_title       = "Customize ERPNext"
app_publisher   = "Shaasie Solutions"
app_description = "Custom print styles and print formats for ERPNext — Cairo font, RTL support, clean install/uninstall"
app_email       = "support@shaasie.com"
app_license     = "MIT"

# ── Desk assets ───────────────────────────────────────────────────────────────
# app_include_css runs ONLY on the ERPNext desk (/app).
# It never affects website pages, login, or portal.
app_include_css = [
    "https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700&display=swap",
    "/assets/customize_erpnext/css/desk.css",
]

# ── Lifecycle hooks ───────────────────────────────────────────────────────────
after_install   = "customize_erpnext.install.after_install"
after_uninstall = "customize_erpnext.install.after_uninstall"

# ── Fixtures ──────────────────────────────────────────────────────────────────
# Fixtures are imported automatically on `bench migrate` and during after_install.
# Filters must reference only records owned by this app — never user data.
#
# HOW TO ADD A NEW PRINT FORMAT:
#   1. Create the Print Format inside ERPNext (desk → Print Format doctype).
#   2. Export it:
#        bench --site <site> export-fixtures --app customize_erpnext
#   3. Add its name to the list below and to PRINT_FORMATS in install.py.
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
    #         "CE Quotation",
    #         # add more names here …
    #     ]]],
    # },
]
