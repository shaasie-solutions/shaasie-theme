/**
 * Customize ERPNext — Theme Switcher
 *
 * Fixes theme persistence across page refreshes by:
 *   1. Reading the saved CE theme from localStorage immediately on load
 *      (before Frappe's ThemeSwitcher can override it).
 *   2. Overriding fetch_themes() to add CE themes to the avatar menu.
 *   3. Overriding set_theme() to save CE themes to localStorage and
 *      apply data-theme directly, skipping Frappe's built-in validation
 *      which would reject unknown theme names and fall back to "light".
 */

(function () {
	var CE_KEY = "ce_desk_theme";

	// ── Step 1: Apply CE theme IMMEDIATELY from localStorage ─────────
	// Runs synchronously before anything else — before Frappe boots,
	// before ThemeSwitcher loads, before any AJAX calls.
	try {
		var saved = localStorage.getItem(CE_KEY);
		if (saved && saved.startsWith("ce_")) {
			document.documentElement.setAttribute("data-theme", saved);
		}
	} catch (e) {}

	// ── Step 2: Override ThemeSwitcher once Frappe is ready ──────────
	function tryOverride() {
		if (
			typeof frappe !== "undefined" &&
			frappe.ui &&
			frappe.ui.ThemeSwitcher
		) {
			// Sync localStorage with server-side desk_theme from boot data
			try {
				var bootTheme =
					frappe.boot &&
					frappe.boot.user &&
					frappe.boot.user.desk_theme;
				if (bootTheme && bootTheme.startsWith("ce_")) {
					localStorage.setItem(CE_KEY, bootTheme);
					document.documentElement.setAttribute("data-theme", bootTheme);
				} else if (bootTheme && !bootTheme.startsWith("ce_")) {
					// User switched back to a built-in theme — clear our storage
					localStorage.removeItem(CE_KEY);
				}
			} catch (e) {}

			// Override the ThemeSwitcher class
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
							// ── CE Themes ──────────────────────
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

				set_theme(theme_name) {
					if (!theme_name) {
						theme_name =
							(frappe.boot &&
								frappe.boot.user &&
								frappe.boot.user.desk_theme) ||
							"light";
					}

					if (theme_name.startsWith("ce_")) {
						// CE theme: apply directly and save to localStorage
						document.documentElement.setAttribute(
							"data-theme",
							theme_name
						);
						this.current_theme = theme_name;
						localStorage.setItem(CE_KEY, theme_name);
						return;
					}

					// Built-in theme: clear our storage and let Frappe handle it
					localStorage.removeItem(CE_KEY);
					return super.set_theme(theme_name);
				}
			};
		} else {
			setTimeout(tryOverride, 200);
		}
	}

	tryOverride();
})();
