# AI Context — atlys-python (PUBLIK)

> Repo ini PUBLIK. Python SDK untuk Atlys API. Package `atlys` di PyPI.

## Fungsi repo ini

Ini **toolkit Python** untuk pakai Atlys API. Isinya:
- Package `atlys` (zero dependency, stdlib `urllib` saja)
- Class `Atlys` + `get()` generik + 27 helper (7 namespace: info, islami, tools, fun, data, osint, downloader)
- Exception ber-tipe: `AuthError`, `NotFoundError`, `ValidationError`, `RateLimitError`, `ServerError`
- Auto-retry 429, mode demo

## Hubungan dengan repo lain

| Repo | Hubungan |
|------|----------|
| `adiprmx/osint-api` (privat) | Dapur utama. SDK ini adalah klien dari API tersebut. |
| `adiprmx/atlys-js` (publik) | SDK JavaScript (saudara kandung, fitur setara). |

## Aturan kerja di repo ini

1. **Setiap update kode → otomatis bump versi + publish PyPI + update repo GitHub.** (Aturan tetap Adip 2026-10-17.)
2. Prefix API key: `atlys_` (sudah diupdate dari `aclys_` typo).
3. Zero dependency — jangan tambah dependensi eksternal.
4. API base: `https://api.atlys.my.id`, auth via header `x-api-key`.

## Status

- v0.1.0 sudah rilis di repo.
- **Belum publish ke PyPI** (butuh token PyPI Adip).

---
*Update dokumen ini setiap ada keputusan baru. Terakhir: 2026-10-19.*
