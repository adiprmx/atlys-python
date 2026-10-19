"""OSINT endpoints: DNS and WHOIS lookups (public data only)."""


class Osint:
    def __init__(self, client):
        self._c = client

    def dns(self, domain):
        """DNS records for a domain, e.g. ``dns("example.com")``."""
        return self._c.get("/v1/osint/dns", {"domain": domain})

    def whois(self, domain):
        """WHOIS/RDAP data for a domain, e.g. ``whois("example.com")``."""
        return self._c.get("/v1/osint/whois", {"domain": domain})
