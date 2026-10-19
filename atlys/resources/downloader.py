"""Downloader endpoints (only for content you have rights to)."""


class Downloader:
    def __init__(self, client):
        self._c = client

    def tiktok(self, url):
        """Resolve a TikTok URL to downloadable media metadata."""
        return self._c.get("/v1/downloader/tiktok", {"url": url})

    def dl(self, url):
        """Universal media downloader metadata for a URL."""
        return self._c.get("/v1/downloader/dl", {"url": url})
