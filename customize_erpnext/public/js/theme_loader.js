/**
 * Customize ERPNext — Theme Loader
 *
 * Runs after frappe.boot is ready.
 * Reads the chosen theme from frappe.boot.ce_desk_theme (set by boot.py)
 * and injects the matching CSS file into the page.
 *
 * Admin changes the theme in: Settings → System Settings → CE Desk Theme
 * Then saves and reloads the page.
 */

frappe.ready(function () {
	var theme = ((frappe.boot && frappe.boot.ce_desk_theme) || "blue").toLowerCase();
	var validThemes = ["blue", "green", "red"];

	// Fallback to blue if an unknown value is stored
	if (!validThemes.includes(theme)) {
		theme = "blue";
	}

	// Avoid injecting twice (e.g. on hot-reload in dev mode)
	if (document.getElementById("ce-desk-theme")) {
		return;
	}

	var link = document.createElement("link");
	link.rel  = "stylesheet";
	link.type = "text/css";
	link.href = "/assets/customize_erpnext/css/theme_" + theme + ".css";
	link.id   = "ce-desk-theme";

	document.head.appendChild(link);
});
