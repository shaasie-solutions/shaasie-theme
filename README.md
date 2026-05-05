# Customize ERPNext

A Frappe/ERPNext app that ships **custom print styles** and **custom print formats** — Cairo font, full RTL/LTR support, and a clean install/uninstall lifecycle.

---

## What It Does

| Feature | Details |
|---------|---------|
| **Desk Theme** | Cairo font loaded on the ERPNext desk (`/app`) via `app_include_css`. Never touches website, portal, or login pages. |
| **Brand Colour** | Primary blue `#005eb8` applied through Frappe CSS variables — dark-mode safe. |
| **Print Style** | `CE Print Style` — Cairo font, coloured table headers, RTL-aware. Select it in any print dialog. |
| **Print Formats** | Five ready-to-use Jinja2 formats: Sales Invoice, Quotation, Sales Order, Purchase Order, Delivery Note. |
| **RTL Support** | All print formats auto-detect `doc.language == 'ar'` and flip direction, alignment, and text. |
| **Clean Uninstall** | Removing the app deletes every record it created — no orphaned data left behind. |

---

## Requirements

- Frappe Framework **v14 or v15**
- ERPNext **v14 or v15**
- Python **3.10+**

---

## Installation

```bash
# 1. Get the app (from local path or GitHub)
bench get-app customize_erpnext /path/to/customize_erpnext
# or
bench get-app customize_erpnext https://github.com/your-org/customize_erpnext

# 2. Install on a site
bench --site your-site.localhost install-app customize_erpnext

# 3. Run migrate to import fixtures
bench --site your-site.localhost migrate
```

After installation you will find:
- **Print Style** → `CE Print Style` in Frappe Print Settings
- **Print Formats** → `CE Sales Invoice`, `CE Quotation`, `CE Sales Order`, `CE Purchase Order`, `CE Delivery Note`

---

## Using the Print Formats

1. Open any Sales Invoice, Quotation, etc.
2. Click **Print**
3. Select the matching **CE** format from the Print Format dropdown
4. Optionally select **CE Print Style** from the Print Style dropdown
5. Print or download as PDF

For Arabic documents, set `Language = Arabic` on the document — the format will automatically switch to RTL.

---

## Uninstallation

```bash
# Remove from the site (deletes all CE records cleanly)
bench --site your-site.localhost remove-app customize_erpnext

# Optionally remove from bench
bench remove-app customize_erpnext
```

The `after_uninstall` hook deletes:
- Print Style: `CE Print Style`
- Print Formats: `CE Sales Invoice`, `CE Quotation`, `CE Sales Order`, `CE Purchase Order`, `CE Delivery Note`

No other data is touched.

---

## Development

### Exporting Updated Fixtures

After modifying a print format or print style in the browser, export updated fixtures:

```bash
bench --site your-site.localhost export-fixtures --app customize_erpnext
```

This writes the updated JSON back to `customize_erpnext/fixtures/`.

### Importing Fixtures Manually

```bash
bench --site your-site.localhost migrate
```

Frappe's migrate command re-imports all fixture files defined in `hooks.py`.

### Project Structure

```
customize_erpnext/
├── __init__.py          # App version
├── hooks.py             # App metadata, assets, fixture declarations, lifecycle hooks
├── install.py           # after_install and after_uninstall functions
├── modules.txt          # Module list (required by Frappe)
├── patches.txt          # Migration patches (future use)
├── fixtures/
│   ├── print_style.json # CE Print Style record
│   └── print_format.json# 5 CE Print Format records (Jinja2 HTML)
└── public/
    └── css/
        └── desk.css     # Desk theme (brand colour + Cairo font)
```

---

## Customisation

### Changing the Brand Colour

Edit `customize_erpnext/public/css/desk.css` and update `--primary-color`:

```css
:root {
  --primary-color: #005eb8; /* change this */
  --primary-dark:  #004494; /* darker shade for hover */
}
```

Then run `bench build --app customize_erpnext`.

### Adding a New Print Format

1. Create the print format in ERPNext (Print Format doctype).
2. Export it: `bench --site site export-fixtures --app customize_erpnext`
3. Add its name to the `fixtures` filter list in `hooks.py`.
4. Add its name to `PRINT_FORMATS` in `install.py` (for clean uninstall).

### Modifying Print Format HTML

Edit the `html` field inside `customize_erpnext/fixtures/print_format.json`.
Templates use standard Jinja2 with access to `doc`, `frappe`, and `_()` (translation).

---

## Safety Notes

- All fixture names are prefixed with `CE` to avoid conflicts with ERPNext's standard formats.
- Fixtures use exact-name filters — they never overwrite or delete third-party records.
- `app_include_css` only loads on `/app` — never on the website or login page.
- All database operations in lifecycle hooks are wrapped in try/except with proper logging.

---

## License

MIT — see [LICENSE](LICENSE).
