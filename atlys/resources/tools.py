"""Tools endpoints: QR, shortlink, headers, extraction, encoding."""


class Tools:
    def __init__(self, client):
        self._c = client

    def qr(self, teks):
        """Generate a QR code image for ``teks`` (returns image bytes/meta)."""
        return self._c.get("/v1/tools/qr", {"teks": teks})

    def shortlink(self, url):
        """Shorten a URL."""
        return self._c.get("/v1/tools/shortlink", {"url": url})

    def cek_header(self, url):
        """Inspect HTTP response headers of a URL."""
        return self._c.get("/v1/tools/cek-header", {"url": url})

    def extract(self, url):
        """Extract readable article text from a URL."""
        return self._c.get("/v1/tools/extract", {"url": url})

    def encode(self, teks, metode="base64"):
        """Encode text (``base64``, ``url``, ``hex``)."""
        return self._c.get("/v1/tools/encode",
                           {"teks": teks, "metode": metode})

    def decode(self, teks, metode="base64"):
        """Decode text (``base64``, ``url``, ``hex``)."""
        return self._c.get("/v1/tools/decode",
                           {"teks": teks, "metode": metode})
