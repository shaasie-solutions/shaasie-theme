/**
 * Customize ERPNext — Theme Switcher
 *
 * Extends Frappe's built-in ThemeSwitcher to add CE Blue, CE Green,
 * and CE Red to the avatar menu — exactly where Light and Dark appear.
 *
 * Uses a retry loop instead of frappe.ready() for compatibility
 * across Frappe v14 and v15.
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
						{
							name: "light",
							label: "Frappe Light",
							info: "Light Theme",
						},
						{
							name: "dark",
							label: "Timeless Night",
							info: "Dark Theme",
						},
						{
							name: "automatic",
							label: "Automatic",
							info: "Follows your system setting",
						},
						// ── CE Themes ──────────────────────────
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
	} else {
		// frappe.ui.ThemeSwitcher not ready yet — retry in 200ms
		setTimeout(tryOverride, 200);
	}
})();
