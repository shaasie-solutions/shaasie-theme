/**
 * Customize ERPNext — Theme Switcher
 *
 * What was wrong before:
 *   Frappe's toggle_theme("ce_blue") calls toTitle() before sending to
 *   Python, so Python received "Ce_blue" not "ce_blue". Our allow-list
 *   didn't match, nothing was saved to the DB, and on refresh Frappe
 *   rendered the old theme from the database — causing the reset.
 *
 * The real fix is in overrides/switch_theme.py (normalize theme name).
 * This JS file only needs to add CE themes to the avatar-menu picker.
 *
 * Flow after the fix:
 *   1. User picks CE Blue  →  toggle_theme("ce_blue")
 *   2. Frappe sets data-theme-mode="ce_blue" in DOM
 *   3. Frappe's MutationObserver fires frappe.ui.set_theme()
 *   4. set_theme reads data-theme-mode → sets data-theme="ce_blue" ✅
 *   5. Python switch_theme receives "Ce_blue", normalises → saves "ce_blue"
 *   6. On next page load Frappe renders data-theme-mode="ce_blue" in HTML
 *   7. set_theme() runs on startup → data-theme="ce_blue" ✅  no reset!
 */

(function tryOverride() {
	if (
		typeof frappe !== "undefined" &&
		frappe.ui &&
		frappe.ui.ThemeSwitcher
	) {
		frappe.ui.ThemeSwitcher = class CEThemeSwitcher extends frappe.ui.ThemeSwitcher {
			fetch_themes() {
				return new Promise((resolve) => {
					this.themes = [
						{ name: "light",     label: "Frappe Light", info: "Light Theme"                 },
						{ name: "dark",      label: "Timeless Night", info: "Dark Theme"                },
						{ name: "automatic", label: "Automatic",    info: "Follows your system setting" },
						// ── CE Themes ────────────────────────────────────
						{ name: "ce_blue",  label: "CE Blue",  info: "Cairo · Blue #005eb8"  },
						{ name: "ce_green", label: "CE Green", info: "Cairo · Green #1a7a4a" },
						{ name: "ce_red",   label: "CE Red",   info: "Cairo · Red #c0392b"   },
					];
					resolve(this.themes);
				});
			}
		};
	} else {
		setTimeout(tryOverride, 200);
	}
})();
