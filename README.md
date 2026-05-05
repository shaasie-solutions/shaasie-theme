# Customization

A Frappe/ERPNext app that ships **custom desk themes**, a **custom print style**, and a clean foundation for adding **custom print formats** — Cairo font, RTL/LTR support, and a safe install/uninstall lifecycle.

---

## What It Does

| Feature | Details |
|---------|---------|
| **3 Desk Themes** | CE Blue, CE Green, CE Red — appear in the avatar menu alongside Frappe's built-in Light and Dark themes. Cairo font included in every theme. |
| **Print Style** | `CE Print Style` — Cairo font, branded table headers, RTL-aware. Select it in any print dialog. |
| **Print Format Foundation** | No formats bundled — each format is added per-client via the `export-fixtures` workflow (see Development section). |
| **RTL Support** | All CE themes and print style detect Arabic and flip direction automatically. |
| **Clean Uninstall** | Removing the app deletes every record it created — no orphaned data left behind. |

---

## Requirements

- Frappe Framework **v14 or v15**
- ERPNext **v14 or v15**
- Python **3.10+**

---

## Installation

```bash
# 1. Get the app from GitHub
bench get-app customization https://github.com/shaasie-solutions/customize-erpnext

# 2. Install on a site
bench --site your-site.localhost install-app customization

# 3. Run migrate to import fixtures
bench --site your-site.localhost migrate

# 4. Build assets
bench build --app customization
```

After installation:
- **Desk Themes** → Click avatar (top right) → CE Blue / CE Green / CE Red are listed alongside Light and Dark
- **Print Style** → Open any document → Print → Print Style dropdown → `CE Print Style`

---

## Using the Desk Themes

1. Click your **avatar** (top right of the desk)
2. Select a theme — **CE Blue**, **CE Green**, or **CE Red**
3. The desk changes colour immediately
4. Cairo font is applied automatically with every CE theme
5. Your choice is saved per-user and restored on next login

---

## Using the Print Style

1. Open any document (Sales Invoice, Purchase Order, etc.)
2. Click **Print**
3. Select **CE Print Style** from the Print Style dropdown
4. Print or download as PDF — Cairo font and branded table headers apply

---

## Uninstallation

```bash
# Remove from the site — deletes all CE records cleanly
bench --site your-site.localhost remove-app customization

# Optionally remove from bench entirely
bench remove-app customization
```

The `after_uninstall` hook deletes:
- Print Style: `CE Print Style`
- Print Formats: any formats registered in `install.py → PRINT_FORMATS`

No other site data is touched.

---

## Development

### Project Structure

```
customization/
├── __init__.py              # App version (1.0.0)
├── hooks.py                 # App metadata, assets, overrides, fixtures, lifecycle hooks
├── install.py               # after_install and after_uninstall (idempotent)
├── modules.txt              # Module declaration (required by Frappe)
├── patches.txt              # Migration patches (future use)
├── fixtures/
│   └── print_style.json     # CE Print Style record
├── overrides/
│   ├── __init__.py
│   └── switch_theme.py      # Extends Frappe's switch_theme to accept CE theme names
└── public/
    ├── css/
    │   └── ce_themes.css    # All 3 CE themes in one file — scoped by data-theme attribute
    └── js/
        └── theme_switcher.js# Extends frappe.ui.ThemeSwitcher to add CE themes to avatar menu
```

### How the Theme System Works

```
theme_switcher.js     → adds CE Blue / Green / Red to Frappe's avatar menu
overrides/switch_theme.py → extends Frappe's switch_theme to save CE theme names
ce_themes.css         → CSS scoped to [data-theme="ce_blue"] etc. — Frappe sets this on <html>
```

### Adding a New Print Format

1. Create the Print Format inside ERPNext (desk → Print Format doctype)
2. Add its name to `hooks.py → fixtures → "Print Format"` filter list
3. Add its name to `install.py → PRINT_FORMATS` list
4. Export:
   ```bash
   bench --site your-site.localhost export-fixtures --app customization
   ```
5. Commit and push:
   ```bash
   git add -A
   git commit -m "feat: add CE Sales Invoice print format"
   git push
   ```

### Modifying a Theme Colour

Edit `customization/public/css/ce_themes.css` — find the `[data-theme="ce_blue"]` block and update the colour values. Then rebuild:

```bash
bench build --app customization
bench --site your-site.localhost clear-cache
```

### Adding a New Theme

1. Add a new block to `ce_themes.css`:
   ```css
   [data-theme="ce_purple"] {
       --primary: #6a0dad;
       ...
   }
   ```
2. Add it to the themes list in `theme_switcher.js`
3. Add `"ce_purple"` to the `allowed_themes` set in `overrides/switch_theme.py`
4. Build and clear cache

### Exporting Updated Print Style

After editing `CE Print Style` in the browser:

```bash
bench --site your-site.localhost export-fixtures --app customization
git add -A && git commit -m "style: update CE Print Style"
git push
```

---

## Safety Notes

- All CE records are prefixed with `CE` — zero conflict with ERPNext standard records
- Fixtures use exact-name filters — they never overwrite or delete third-party records
- `app_include_css` and `app_include_js` load only on `/app` — never on website, portal, or login
- The `switch_theme` override is additive — Frappe's built-in themes (Light, Dark, Automatic) continue to work normally
- All database operations in lifecycle hooks are wrapped in try/except with `frappe.log_error`

---

## License

MIT — see [LICENSE](LICENSE).
