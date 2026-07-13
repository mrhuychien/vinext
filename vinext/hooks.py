"""Frappe app hooks for vinext (Vietnamese Language Pack).

vinext is a translation-only Frappe app. It ships a single asset — the
Vietnamese translation catalogue at ``vinext/translations/vi.csv`` — which
Frappe loads automatically for the ``vi`` language. There are no DocTypes,
controllers, scheduler jobs, or client scripts; this module only declares
the app metadata Frappe needs to recognise and install the package.
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
