# Shaasie Theme

A minimal ERPNext / Frappe app that applies:
- **Cairo font** to the ERPNext desk
- **Brand colour tokens** via Frappe CSS variables
- **Print style** (Shaasie Style) for clean Arabic/English documents

No login-page overrides. No leftover tables or files after uninstall.

---

## Install

```bash
bench get-app https://github.com/shaasie-solutions/shaasie-theme
bench --site your-site.local install-app shaasie_theme
bench --site your-site.local migrate
```

## Uninstall

```bash
bench --site your-site.local uninstall-app shaasie_theme
```

The app removes the **Shaasie Style** print style automatically on uninstall.

---

## What it does

| Feature | Details |
|---|---|
| Font | Cairo (Google Fonts) — loaded only on the desk (`/app`) |
| Colours | `--primary-color: #005eb8` via CSS variables |
| Print Style | "Shaasie Style" — Cairo font, clean table headers |
| Login page | **Stock Frappe** — untouched |

## App info

- **App name**: `shaasie_theme`
- **Publisher**: Shaasie Solutions
- **License**: MIT
