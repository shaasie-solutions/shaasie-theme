/**
 * Customize ERPNext — Theme Switcher
 *
 * Problem: On refresh Frappe reads desk_theme from boot data, looks for
 * "ce_blue" in its built-in theme list, doesn't find it, and resets to
 * "light" — AFTER our script already applied the CE theme.
 *
 * Solution (3 layers):
 *   1. Apply CE theme from localStorage instantly (before Frappe boots).
 *   2. MutationObserver: if Frappe resets data-theme within the first 4s
 *      of page load, restore our CE theme immediately.
 *   3. Override ThemeSwitcher.fetch_themes() and set_theme() so the
 *      avatar menu shows CE themes and switching saves to localStorage.
 */

(function () {
	var CE_KEY   = "ce_desk_theme";
	var GUARD_MS = 4000; // ms after page load during which we protect the theme
	var startTime = Date.now();
	var savedTheme = null;

	// ── Layer 1: Apply CE theme immediately from localStorage ────────
	try {
		savedTheme = localStorage.getItem(CE_KEY);
	} catch (e) {}

	if (savedTheme && savedTheme.startsWith("ce_")) {
		document.documentElement.setAttribute("data-theme", savedTheme);
	}

	// ── Layer 2: MutationObserver — guard against Frappe's boot reset ─
	// Frappe runs setup_theme() after the boot AJAX call returns and may
	// reset data-theme. We watch for that and immediately restore ours.
	if (savedTheme && savedTheme.startsWith("ce_")) {
		var observer = new MutationObserver(function (mutations) {
			// After GUARD_MS the page is stable — stop watching
			if (Date.now() - startTime > GUARD_MS) {
				observer.disconnect();
				return;
			}
			for (var i = 0; i < mutations.length; i++) {
				if (mutations[i].attributeName === "data-theme") {
					var current = document.documentElement.getAttribute("data-theme");
					if (current !== savedTheme) {
						// Frappe reset it — restore immediately
						document.documentElement.setAttribute("data-theme", savedTheme);
					}
				}
			}
		});

		observer.observe(document.documentElement, {
			attributes:       true,
			attributeFilter:  ["data-theme"],
		});
	}

	// ── Layer 3: Override ThemeSwitcher (avatar menu + switching) ─────
	function tryOverride() {
		if (
			typeof frappe !== "undefined" &&
			frappe.ui &&
			frappe.ui.ThemeSwitcher
		) {
			// Sync savedTheme with server-side boot data
			try {
				var bootTheme =
					frappe.boot &&
					frappe.boot.user &&
					frappe.boot.user.desk_theme;

				if (bootTheme && bootTheme.startsWith("ce_")) {
					savedTheme = bootTheme;
					localStorage.setItem(CE_KEY, bootTheme);
					document.documentElement.setAttribute("data-theme", bootTheme);
				} else if (bootTheme && !bootTheme.startsWith("ce_")) {
					// User switched back to a built-in theme
					savedTheme = null;
					localStorage.removeItem(CE_KEY);
				}
			} catch (e) {}

			frappe.ui.ThemeSwitcher = class CEThemeSwitcher extends frappe.ui.ThemeSwitcher {
				fetch_themes() {
					return new Promise((resolve) => {
						this.themes = [
							{ name: "light",     label: "Frappe Light", info: "Light Theme"                  },
							{ name: "dark",      label: "Timeless Night", info: "Dark Theme"                 },
							{ name: "automatic", label: "Automatic",    info: "Follows your system setting"  },
							// ── CE Themes ───────────────────────────────
							{ name: "ce_blue",  label: "CE Blue",  info: "Cairo · Blue #005eb8"  },
							{ name: "ce_green", label: "CE Green", info: "Cairo · Green #1a7a4a" },
							{ name: "ce_red",   label: "CE Red",   info: "Cairo · Red #c0392b"   },
						];
						resolve(this.themes);
					});
				}

				set_theme(theme_name) {
					if (!theme_name) {
						theme_name =
							(frappe.boot && frappe.boot.user && frappe.boot.user.desk_theme) ||
							"light";
					}

					if (theme_name.startsWith("ce_")) {
						savedTheme = theme_name;
						document.documentElement.setAttribute("data-theme", theme_name);
						this.current_theme = theme_name;
						try { localStorage.setItem(CE_KEY, theme_name); } catch (e) {}
						return; // do NOT call super — it would reset the theme
					}

					// Built-in theme selected: clear CE storage
					savedTheme = null;
					try { localStorage.removeItem(CE_KEY); } catch (e) {}
					return super.set_theme(theme_name);
				}
			};
		} else {
			setTimeout(tryOverride, 200);
		}
	}

	tryOverride();
})();
