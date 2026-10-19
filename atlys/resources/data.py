"""Data endpoints: postal codes and administrative regions (Indonesia)."""


class Data:
    def __init__(self, client):
        self._c = client

    def kodepos(self, kode):
        """Look up a postal code, e.g. ``kodepos("10110")``."""
        return self._c.get("/v1/data/kodepos", {"kode": kode})

    def kodepos_kecamatan(self, slug, limit=20):
        """Postal codes in a district,
        e.g. ``kodepos_kecamatan("gambir")``."""
        return self._c.get("/v1/data/kodepos/kecamatan/" + slug,
                           {"limit": limit})

    def kodepos_kelurahan(self, slug, limit=20):
        """Postal codes in a sub-district,
        e.g. ``kodepos_kelurahan("menteng")``."""
        return self._c.get("/v1/data/kodepos/kelurahan/" + slug,
                           {"limit": limit})

    def wilayah_kecamatan(self, slug, limit=20):
        """Villages in a district, e.g. ``wilayah_kecamatan("gambir")``."""
        return self._c.get("/v1/data/wilayah/kecamatan/" + slug,
                           {"limit": limit})

    def wilayah_kota(self, slug, limit=20):
        """Districts in a city, e.g. ``wilayah_kota("jakarta-pusat")``."""
        return self._c.get("/v1/data/wilayah/kota/" + slug,
                           {"limit": limit})
