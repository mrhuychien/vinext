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


def set_site_language():
	"""Switch the whole site to Vietnamese, the way erpnextvn's setup does.

	`System Settings.language` is a plain Link with no enabled-filter, so
	writing it directly sidesteps the picker entirely — useful on a site that
	never went through the Setup Wizard. Deliberately NOT called from
	`after_install`: installing a translation catalogue should not silently
	re-language a running site. Run it explicitly:

	    bench --site <site> execute vinext.install.set_site_language
	"""
	enable_vietnamese()
	frappe.db.set_single_value("System Settings", "language", LANGUAGE_CODE)
	frappe.db.commit()
	frappe.clear_cache()


def diagnose():
	"""Report every link in the chain between the CSV on disk and the UI.

	Run when translations do not show up:

	    bench --site <site> execute vinext.install.diagnose

	Frappe core ships almost no Vietnamese of its own (frappe/locale/vi.po has
	a handful of entries), so essentially all Desk chrome comes from this CSV.
	If `csv keys loaded` is 0 the catalogue is not being read at all, and the
	line above it says why.
	"""
	import os

	from frappe.translate import get_translations_from_apps, get_translations_from_csv

	installed = frappe.get_installed_apps()
	print(f"installed apps          : {installed}")
	print(f"vinext in installed apps: {'vinext' in installed}")

	try:
		path = frappe.get_app_path("vinext", "translations", "vi.csv")
	except Exception as exc:  # app not importable / not on the bench
		print(f"get_app_path FAILED     : {exc!r}")
		return
	print(f"catalogue path          : {path}")
	print(f"catalogue exists        : {os.path.exists(path)}")

	from_csv = get_translations_from_csv(LANGUAGE_CODE, "vinext") or {}
	print(f"csv keys loaded         : {len(from_csv)}")
	print(f"  sample 'Submit'       : {from_csv.get('Submit')!r}")

	merged = get_translations_from_apps(LANGUAGE_CODE) or {}
	print(f"merged keys (all apps)  : {len(merged)}")
	print(f"  sample 'Submit'       : {merged.get('Submit')!r}")

	lang_doc = frappe.db.get_value(
		"Language", LANGUAGE_CODE, ["name", "enabled"], as_dict=True
	)
	print(f"Language record         : {lang_doc}")
	print(f"System Settings.language: {frappe.db.get_single_value('System Settings', 'language')!r}")
	print(f"session user language   : {frappe.db.get_value('User', frappe.session.user, 'language')!r}")
