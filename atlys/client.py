"""Core HTTP client for the Atlys API (zero third-party dependencies)."""

import json
import time
import urllib.error
import urllib.parse
import urllib.request

from .errors import RateLimitError, raise_for_response

DEFAULT_BASE_URL = "https://api.atlys.my.id"
DEFAULT_TIMEOUT = 30


class Atlys:
    """Client for https://api.atlys.my.id.

    Args:
        api_key: your API key (``atlys_...``). Optional — without a key
            only demo endpoints work.
        base_url: override the API base URL (default:
            ``https://api.atlys.my.id``).
        timeout: per-request timeout in seconds (default 30).
        auto_retry: automatically retry on HTTP 429 using the
            ``retry-after`` header with exponential backoff (default True).
        max_retries: max retries for a single request (default 3).

    Example:
        >>> from atlys import Atlys
        >>> c = Atlys("atlys_...")
        >>> resp = c.info.gempa()
        >>> print(resp["result"])
    """

    def __init__(self, api_key=None, base_url=DEFAULT_BASE_URL,
                 timeout=DEFAULT_TIMEOUT, auto_retry=True, max_retries=3):
        self.api_key = api_key
        self.base_url = (base_url or DEFAULT_BASE_URL).rstrip("/")
        self.timeout = timeout
        self.auto_retry = auto_retry
        self.max_retries = max_retries
        self._demo = False

        # Resource namespaces (lazy to avoid circulars).
        from .resources import data as _data
        from .resources import downloader as _downloader
        from .resources import fun as _fun
        from .resources import info as _info
        from .resources import islami as _islami
        from .resources import osint as _osint
        from .resources import tools as _tools
        self.info = _info.Info(self)
        self.islami = _islami.Islami(self)
        self.tools = _tools.Tools(self)
        self.fun = _fun.Fun(self)
        self.data = _data.Data(self)
        self.osint = _osint.Osint(self)
        self.downloader = _downloader.Downloader(self)

    @classmethod
    def demo(cls, **kwargs):
        """Return a key-less client pinned to the ``/v1/demo/`` endpoints.

        Demo endpoints return sample data and never require an API key.
        """
        inst = cls(api_key=None, **kwargs)
        inst._demo = True
        return inst

    # -- low-level request machinery ------------------------------------

    def _build_url(self, path, params):
        if self._demo and path.startswith("/v1/") \
                and not path.startswith("/v1/demo/"):
            path = "/v1/demo" + path[len("/v1"):]
        url = self.base_url + path
        if params:
            qs = urllib.parse.urlencode(
                {k: v for k, v in params.items() if v is not None})
            if qs:
                url += "?" + qs
        return url

    def _request(self, method, path, params=None, data=None):
        url = self._build_url(path, params)
        body = None
        headers = {
            "Accept": "application/json",
            "User-Agent": "atlys-python/0.1.0",
        }
        if self.api_key:
            headers["x-api-key"] = self.api_key
        if data is not None:
            body = json.dumps(data).encode("utf-8")
            headers["Content-Type"] = "application/json"

        attempt = 0
        while True:
            req = urllib.request.Request(url, data=body, headers=headers,
                                         method=method)
            try:
                with urllib.request.urlopen(req,
                                            timeout=self.timeout) as resp:
                    return self._parse(resp.status, resp.headers,
                                       resp.read())
            except urllib.error.HTTPError as exc:
                payload = None
                try:
                    payload = json.loads(
                        exc.read().decode("utf-8", "replace"))
                except Exception:
                    payload = None
                headers_map = dict(exc.headers or {})
                if exc.code == 429 and self.auto_retry \
                        and attempt < self.max_retries:
                    wait = self._backoff(headers_map, attempt)
                    attempt += 1
                    time.sleep(wait)
                    continue
                raise_for_response(exc.code, payload, headers_map)
            except urllib.error.URLError as exc:
                raise ConnectionError(
                    "could not reach %s: %s" % (self.base_url, exc.reason))

    def _backoff(self, headers, attempt):
        raw = headers.get("retry-after") or headers.get("Retry-After")
        if raw:
            try:
                return max(1, int(str(raw).split(",")[0].strip()))
            except (ValueError, TypeError):
                pass
        return min(60, 2 ** attempt)

    @staticmethod
    def _parse(status, headers, raw):
        try:
            return json.loads(raw.decode("utf-8", "replace"))
        except Exception:
            raise_for_response(status, None, dict(headers or {}))

    # -- public generic methods ------------------------------------------

    def get(self, path, params=None):
        """Call any GET endpoint, e.g. ``get("/v1/info/gempa")``.

        Returns the full PRD response dict; your data lives in
        ``["result"]``. Works for all ~100,000 endpoints.
        """
        return self._request("GET", path, params=params)

    def post(self, path, data=None, params=None):
        """Call any POST endpoint. Returns the full PRD response dict."""
        return self._request("POST", path, params=params, data=data)
