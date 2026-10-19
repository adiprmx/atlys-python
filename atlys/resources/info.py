"""Info endpoints: news, Hacker News, earthquakes, exchange rates."""


class Info:
    def __init__(self, client):
        self._c = client

    def news(self, limit=10):
        """Latest Indonesian news (auto-scraped, refreshed hourly)."""
        return self._c.get("/v1/info/news", {"limit": limit})

    def hn(self, limit=10):
        """Latest Hacker News stories."""
        return self._c.get("/v1/info/hn", {"limit": limit})

    def sources(self):
        """List the news sources the scraper reads from."""
        return self._c.get("/v1/info/sources")

    def gempa(self):
        """Latest earthquake data (BMKG)."""
        return self._c.get("/v1/info/gempa")

    def kurs(self):
        """Currency exchange rates (IDR base)."""
        return self._c.get("/v1/info/kurs")

    def cuaca(self, kota):
        """Weather for an Indonesian city, e.g. ``cuaca("jakarta")``."""
        return self._c.get("/v1/info/cuaca", {"kota": kota})
