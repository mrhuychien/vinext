"""Post-install setup for the Vietnamese language pack.

Frappe ships the `vi` Language record **disabled** — `frappe/geo/languages.csv`
carries the row `vi,Tiếng Việt,0` — and `frappe.translate.get_all_languages()`,
which populates the language pickers, filters on `enabled = 1`. So a freshly
installed language pack stays invisible until that record is switched on.
Enabling it is the one piece of setup this app performs.
"""

import frappe

LANGUAGE_CODE = "vi"
LANGUAGE_NAME = "Tiếng Việt"


def after_install():
	enable_vietnamese()


def enable_vietnamese():
	"""Make `vi` selectable in System Settings and the user language picker.

	Saving through the document (rather than `db.set_value`) lets
	`Language.on_update` drop the `languages` / `languages_with_name` caches
	that `get_all_languages()` reads, so the language appears without a
	restart.
	"""
	if frappe.db.exists("Language", LANGUAGE_CODE):
		doc = frappe.get_doc("Language", LANGUAGE_CODE)
		if doc.enabled:
			return
		doc.enabled = 1
		doc.save(ignore_permissions=True)
	else:
		# Only reachable on a site that predates the language in languages.csv.
		frappe.get_doc(
			{
				"doctype": "Language",
				"language_code": LANGUAGE_CODE,
				"language_name": LANGUAGE_NAME,
				"enabled": 1,
			}
		).insert(ignore_permissions=True)

	frappe.db.commit()
