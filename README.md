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
bench build
```

Then set the language to **Vietnamese** in *Settings → My Settings* (per user)
or *System Settings → Language* (site-wide). Translations apply on the next
page reload.

### How it works

Frappe scans every installed app for `<app>/translations/<lang>.csv` and merges
the entries into the runtime translation map. Because `vinext` ships only that
file, installing it simply adds/overrides the Vietnamese strings — nothing else
changes on your site. Uninstalling removes them again.

### CSV format

```csv
Source,Translation,Context
Submit,Xác nhận,
Cancel,Hủy,
Draft,Nháp,
```

- **Source** — the untranslated English string as it appears in the code.
- **Translation** — the Vietnamese rendering.
- **Context** — optional disambiguation context (usually blank).

To extend the pack, append rows to `vinext/translations/vi.csv` and reinstall or
run `bench --site your-site clear-cache`.

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
bench build
```

Sau đó đặt ngôn ngữ **Tiếng Việt** trong *Settings → My Settings* (theo từng
người dùng) hoặc *System Settings → Language* (toàn site). Bản dịch có hiệu lực
khi tải lại trang.

### Cơ chế hoạt động

Frappe quét mọi app đã cài để tìm file `<app>/translations/<lang>.csv` rồi gộp
các dòng vào bảng dịch runtime. Vì `vinext` chỉ vận chuyển file đó, cài app
đơn thuần là thêm/ghi đè các chuỗi tiếng Việt — không thay đổi gì khác trên
site. Gỡ app sẽ xóa chúng đi.

### Định dạng CSV

```csv
Source,Translation,Context
Submit,Xác nhận,
Cancel,Hủy,
Draft,Nháp,
```

- **Source** — chuỗi tiếng Anh gốc trong code.
- **Translation** — bản dịch tiếng Việt.
- **Context** — ngữ cảnh để phân biệt (thường để trống).

Muốn bổ sung, thêm dòng vào `vinext/translations/vi.csv` rồi cài lại hoặc chạy
`bench --site your-site clear-cache`.

---

## License

GPL-3.0-or-later. See [LICENSE](LICENSE).
