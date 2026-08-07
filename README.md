# ViNext — vinext

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Frappe v15+](https://img.shields.io/badge/Frappe-v15%2B-green.svg)](https://frappeframework.com)

**Vietnamese Language Pack for Frappe / ERPNext** — gói ngôn ngữ tiếng Việt thuần túy.

---

## 🇬🇧 English

`vinext` is a **translation-only** Frappe app. It ships a single asset — a
Vietnamese translation catalogue (`vinext/translations/vi.csv`, 25k+ entries) —
that Frappe loads automatically for the `vi` language. It contains **no**
DocTypes, controllers, print formats, reports, scheduler jobs, or client
scripts.

Use it when you want Vietnamese UI translations without pulling in a full
localization stack (accounting, e-invoicing, payroll, …). The catalogue was
extracted from [`erpnextvn`](https://github.com/mrhuychien/erpnextvn) and
covers core Frappe, ERPNext, and HRMS terms.

### Install

```bash
# From your bench directory
bench get-app https://github.com/mrhuychien/vinext
bench --site your-site install-app vinext
bench --site your-site clear-cache
bench restart
```

Then set the language to **Vietnamese** in *Settings → My Settings* (per user)
or *System Settings → Language* (site-wide), and **hard-refresh** the browser
(`Ctrl+Shift+R`). Desk strings are delivered through `bootinfo`, so a stale
client-side boot is the usual reason a correct catalogue appears not to apply.

Note: `vi` ships **disabled** in Frappe's `Language` list, so enable the
*Vietnamese* record for it to be selectable in the picker. `bench build` is not
needed — this app ships no JS/CSS, and CSV translations need no compile step.

### How it works

Frappe scans every installed app for `<app>/translations/<lang>.csv` and merges
the entries into the runtime translation map. Because `vinext` ships only that
file, installing it simply adds/overrides the Vietnamese strings — nothing else
changes on your site. Uninstalling removes them again.

This is still a live code path in **Frappe v16** — gettext PO was added
*alongside* the CSV loader, not as a replacement
([`frappe/translate.py`](https://github.com/frappe/frappe/blob/v16.16.0/frappe/translate.py#L172-L193)):

```python
for app in apps or frappe.get_installed_apps(_ensure_on_bench=True):
    translations.update(get_translations_from_csv(lang, app) or {})
    translations.update(get_translations_from_mo(lang, app) or {})
```

CSV is read straight off disk on a cache miss, so no compile step is involved.
(Frappe core has moved its own strings to `locale/*.po`; the CSV reader is kept
for third-party apps like this one.)

### CSV format

**No header row** — Frappe parses the file with a plain `csv.reader` and treats
line 1 as data, so a header becomes a bogus `Source:Context` entry:

```csv
Submit,Xác nhận,
Cancel,Hủy,
Draft,Nháp,
```

- **Source** — the untranslated English string exactly as it appears in the code.
- **Translation** — the Vietnamese rendering.
- **Context** — optional disambiguation context (usually blank).

Every row must have **exactly 3 columns**; quote any field containing a comma.
Rows with a different column count are silently discarded *and* write an Error
Log entry on every cache rebuild.

Multi-line source strings need **real** newlines and tabs inside a quoted field.
Frappe expands a literal `\n` into a newline but leaves `\t` untouched, so a
literal `\t` will never match the runtime string.

To extend the pack, append rows to `vinext/translations/vi.csv`, then
`bench --site your-site clear-cache && bench restart` and hard-refresh.

---

## 🇻🇳 Tiếng Việt

`vinext` là app Frappe **chỉ chứa bản dịch**. App vận chuyển đúng một thứ — bộ
từ điển tiếng Việt (`vinext/translations/vi.csv`, hơn 25.000 dòng) — được Frappe
tự động nạp cho ngôn ngữ `vi`. App **không** kèm DocType, controller, mẫu in,
báo cáo, tác vụ nền hay client script.

Dùng app này khi bạn chỉ cần giao diện tiếng Việt mà không muốn cài trọn bộ bản
địa hóa (kế toán, hóa đơn điện tử, tiền lương…). Bộ từ điển được tách ra từ
[`erpnextvn`](https://github.com/mrhuychien/erpnextvn), bao phủ các thuật ngữ
cốt lõi của Frappe, ERPNext và HRMS.

### Cài đặt

```bash
# Từ thư mục bench
bench get-app https://github.com/mrhuychien/vinext
bench --site your-site install-app vinext
bench --site your-site clear-cache
bench restart
```

Sau đó đặt ngôn ngữ **Tiếng Việt** trong *Settings → My Settings* (theo từng
người dùng) hoặc *System Settings → Language* (toàn site), rồi **tải lại trang
cứng** (`Ctrl+Shift+R`). Chuỗi giao diện Desk đi qua `bootinfo`, nên boot cũ còn
cache ở trình duyệt là lý do phổ biến nhất khiến bản dịch đúng mà "không thấy ăn".

Lưu ý: bản ghi `vi` trong danh sách `Language` của Frappe mặc định **tắt**, cần
bật *Vietnamese* thì mới chọn được trong picker. Không cần `bench build` — app
không có JS/CSS, và bản dịch CSV không cần bước biên dịch.

### Cơ chế hoạt động

Frappe quét mọi app đã cài để tìm file `<app>/translations/<lang>.csv` rồi gộp
các dòng vào bảng dịch runtime. Vì `vinext` chỉ vận chuyển file đó, cài app
đơn thuần là thêm/ghi đè các chuỗi tiếng Việt — không thay đổi gì khác trên
site. Gỡ app sẽ xóa chúng đi.

### Định dạng CSV

**Không có dòng tiêu đề** — Frappe đọc file bằng `csv.reader` thuần và coi dòng 1
là dữ liệu, nên tiêu đề sẽ thành một entry rác `Source:Context`:

```csv
Submit,Xác nhận,
Cancel,Hủy,
Draft,Nháp,
```

- **Source** — chuỗi tiếng Anh gốc, đúng y như trong code.
- **Translation** — bản dịch tiếng Việt.
- **Context** — ngữ cảnh để phân biệt (thường để trống).

Mỗi dòng phải có **đúng 3 cột**; trường nào chứa dấu phẩy thì phải bọc nháy kép.
Dòng sai số cột sẽ bị bỏ qua *và* ghi một bản ghi Error Log mỗi lần dựng lại cache.

Chuỗi nhiều dòng cần newline và tab **thật** bên trong trường có nháy kép. Frappe
chỉ đổi `\n` dạng ký tự thành xuống dòng, còn `\t` thì giữ nguyên — nên `\t`
viết dạng ký tự sẽ không bao giờ khớp chuỗi gốc lúc chạy.

Muốn bổ sung, thêm dòng vào `vinext/translations/vi.csv`, rồi chạy
`bench --site your-site clear-cache && bench restart` và tải lại trang cứng.

---

## License

GPL-3.0-or-later. See [LICENSE](LICENSE).
