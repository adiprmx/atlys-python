# atlys — Python SDK untuk Atlys API

Python SDK for the Atlys API — ~100.000 endpoint data publik Indonesia dalam satu REST API.

*English summary below.*

## instalasi

```bash
pip install atlys
```

## mulai cepat

```python
from atlys import Atlys

c = Atlys("aclys_kunci_api_anda")

# helper populer
gempa = c.info.gempa()
print(gempa["result"])

jadwal = c.islami.jadwal_sholat("jakarta")
print(jadwal["result"])

# endpoint apa pun (100.000 tersedia)
hasil = c.get("/v1/data/kodepos/kelurahan/menteng", {"limit": 3})
print(hasil["result"])
```

## tanpa api key (mode demo)

```python
from atlys import Atlys

c = Atlys.demo()  # data contoh, tanpa key
berita = c.info.news(limit=3)
print(berita["result"])
```

## penanganan error

```python
from atlys import Atlys, AuthError, RateLimitError, AtlysError

c = Atlys("aclys_...")

try:
    c.info.news()
except AuthError:
    print("api key salah atau hilang")
except RateLimitError as e:
    print("kena rate limit, coba lagi dalam", e.retry_after, "detik")
except AtlysError as e:
    print("error:", e.code, e.message)
```

Rate limit 429 otomatis di-retry (pakai header `retry-after` + backoff)
kecuali `auto_retry=False`.

## helper yang tersedia

| namespace | method |
|---|---|
| `c.info` | `news()`, `hn()`, `sources()`, `gempa()`, `kurs()`, `cuaca(kota)` |
| `c.islami` | `jadwal_sholat(kota, tanggal)`, `quran(surah, ayat)`, `doa()`, `asmaul_husna()` |
| `c.tools` | `qr(teks)`, `shortlink(url)`, `cek_header(url)`, `extract(url)`, `encode()`, `decode()` |
| `c.fun` | `quote_random()`, `jokes()`, `pantun()`, `fakta_unik()` |
| `c.data` | `kodepos(kode)`, `kodepos_kecamatan(slug)`, `kodepos_kelurahan(slug)`, `wilayah_kecamatan(slug)`, `wilayah_kota(slug)` |
| `c.osint` | `dns(domain)`, `whois(domain)` |
| `c.downloader` | `tiktok(url)`, `dl(url)` |

Untuk endpoint di luar daftar, pakai `c.get("/v1/...")` atau
`c.post("/v1/...", data={...})` — semua ~100.000 endpoint bisa diakses.

## format respons

```python
{
    "status": "ok",
    "creator": "Atlys",
    "result": { ... },        # data yang kamu minta
    "meta": {"cached": False, "ms": 12}
}
```

---

## English

Python SDK for the [Atlys API](https://api.atlys.my.id) — ~100,000 Indonesian
public-data endpoints behind one REST API.

```bash
pip install atlys
```

```python
from atlys import Atlys

c = Atlys("aclys_your_api_key")
print(c.info.gempa()["result"])          # latest earthquakes (BMKG)
print(c.islami.quran(112)["result"])     # surah al-ikhlas
print(c.get("/v1/tools/qr", {"teks": "halo"})["result"])
```

No key? `Atlys.demo()` hits the `/v1/demo/` sample-data endpoints.
Errors raise typed exceptions (`AuthError`, `RateLimitError` with
`retry_after`, `NotFoundError`, `ValidationError`, `ServerError`).

Docs: https://docs.atlys.my.id · Status: https://status.atlys.my.id

## lisensi / license

MIT — lihat `LICENSE`.
