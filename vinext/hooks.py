"""Frappe app hooks for vinext (Vietnamese Language Pack).

vinext is a translation-only Frappe app. It ships a single asset — the
Vietnamese translation catalogue at ``vinext/translations/vi.csv`` — which
Frappe loads automatically for the ``vi`` language. There are no DocTypes,
controllers, scheduler jobs, or client scripts.

The one exception is ``after_install``: Frappe ships the ``vi`` Language record
disabled, and the language pickers only list enabled languages, so the pack
would otherwise install correctly and still be unselectable.
"""

app_name = "vinext"
app_title = "ViNext"
app_publisher = "1nguoi.com"
app_description = "Vietnamese Language Pack for Frappe / ERPNext"
app_email = "hello@1nguoi.com"
app_license = "GPL-3.0"
app_icon = "octicon octicon-globe"
app_color = "#DA251D"  # Vietnamese flag red

# Only Frappe is required — the translations apply to whatever apps
# (frappe, erpnext, hrms, custom apps) happen to be installed on the site.
required_apps = ["frappe"]

# Enable the `vi` Language record, which Frappe ships disabled.
after_install = "vinext.install.after_install"

# Deliberately no `before_uninstall` counterpart: another Vietnamese pack
# (e.g. erpnextvn) may be relying on the same Language record, so removing
# this app must not disable Vietnamese site-wide.
