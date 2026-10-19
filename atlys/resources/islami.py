"""Islami endpoints: prayer times, Quran, doa, asmaul husna."""


class Islami:
    def __init__(self, client):
        self._c = client

    def jadwal_sholat(self, kota, tanggal=None):
        """Prayer schedule for a city, e.g. ``jadwal_sholat("jakarta")``.

        ``tanggal`` is ``YYYY-MM-DD``; defaults to today.
        """
        params = {"kota": kota}
        if tanggal:
            params["tanggal"] = tanggal
        return self._c.get("/v1/islami/jadwal-sholat", params)

    def quran(self, surah, ayat=None):
        """Quran text. ``quran(112)`` for the whole surah,
        ``quran(2, 255)`` for a single verse."""
        params = {"surah": surah}
        if ayat is not None:
            params["ayat"] = ayat
        return self._c.get("/v1/islami/quran", params)

    def doa(self, kategori=None):
        """Collection of doa; filter by ``kategori`` if given."""
        params = {"kategori": kategori} if kategori else None
        return self._c.get("/v1/islami/doa", params)

    def asmaul_husna(self):
        """The 99 names of Allah with meanings."""
        return self._c.get("/v1/islami/asmaul-husna")
