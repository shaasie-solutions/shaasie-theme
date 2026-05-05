/**
 * Customize ERPNext — Theme Switcher
 *
 * Extends Frappe's built-in ThemeSwitcher to add CE Blue, CE Green,
 * and CE Red to the avatar menu → exactly where Light and Dark appear.
 *
 * How it works:
 *   1. We extend frappe.ui.ThemeSwitcher and override fetch_themes().
 *   2. fetch_themes() returns the full list: Frappe's built-in themes
 *      plus our three CE themes.
 *   3. When the user picks a CE theme, Frappe calls switch_theme() on
 *      the server. Our override (overrides/switch_theme.py) accepts
 *      the CE theme names and saves them to the User record.
 *   4. On next load, Frappe reads desk_theme from the User record and
 *      sets data-theme on <html>. ce_themes.css then applies the right
 *      colours and Cairo font.
 *
 * Reference:
 *   https://medium.com/@pratheeshrussell/customising-frappe-erpnext-ui-part-i-adding-a-new-theme-74d7103df275
 */

frappe.ready(function () {
	if (!frappe.ui || !frappe.ui.ThemeSwitcher) return;

	frappe.ui.ThemeSwitcher = class CEThemeSwitcher extends frappe.ui.ThemeSwitcher {
		fetch_themes() {
			return new Promise((resolve) => {
				this.themes = [
					{
						name: "light",
						label: frappe._("Frappe Light"),
						info: frappe._("Light Theme"),
					},
					{
						name: "dark",
						label: frappe._("Timeless Night"),
						info: frappe._("Dark Theme"),
					},
					{
						name: "automatic",
						label: frappe._("Automatic"),
						info: frappe._("Follows your system setting"),
					},
					// ── CE Themes ──────────────────────────────────────
					{
						name: "ce_blue",
						label: "CE Blue",
						info: "Cairo · Blue #005eb8",
					},
					{
						name: "ce_green",
						label: "CE Green",
						info: "Cairo · Green #1a7a4a",
					},
					{
						name: "ce_red",
						label: "CE Red",
						info: "Cairo · Red #c0392b",
					},
				];
				resolve(this.themes);
			});
		}
	};
});
