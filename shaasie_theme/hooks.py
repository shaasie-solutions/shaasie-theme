from . import __version__ as app_version

app_name = "shaasie_theme"
app_title = "Shaasie Theme"
app_publisher = "Shaasie Solutions"
app_description = "Cairo font and print style for ERPNext"
app_email = "support@shaasie.com"
app_license = "MIT"

# ── Desk assets (/app only) ───────────────────────────────────────────────────
# app_include_css loads ONLY on the ERPNext desk — never on website or login pages.
app_include_css = [
    "https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700&display=swap",
    "/assets/shaasie_theme/css/theme.css",
]

# ── Clean uninstall ───────────────────────────────────────────────────────────
after_uninstall = "shaasie_theme.install.after_uninstall"

# ── Fixtures ──────────────────────────────────────────────────────────────────
fixtures = [{"dt": "Print Style", "filters": [["name", "in", ("Shaasie Style",)]]}]
