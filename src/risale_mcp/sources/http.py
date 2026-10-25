"""Siteleri yormayan, istekler arasında bekleyen basit HTTP istemcisi."""

import time
import urllib.error
import urllib.request

USER_AGENT = "risale-mcp/0.1 (kisisel arastirma; nazik indirici)"


class PoliteClient:
    def __init__(self, delay: float, retries: int = 6, timeout: float = 30.0):
        self.delay = delay
        self.retries = retries
        self.timeout = timeout
        self._last_request = 0.0

    def get(self, url: str) -> bytes:
        """URL'yi indirir. 5xx ve ağ hatalarında artan beklemeyle yeniden dener; 4xx hemen hata verir."""
        for attempt in range(1, self.retries + 1):
            self._wait()
            request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            try:
                with urllib.request.urlopen(request, timeout=self.timeout) as response:
                    return response.read()
            except urllib.error.HTTPError as error:
                if error.code < 500 or attempt == self.retries:
                    raise
            except OSError:  # bağlantı hatası, okuma zaman aşımı (URLError, TimeoutError…)
                if attempt == self.retries:
                    raise
            time.sleep(self.delay * 2 ** attempt)
        raise AssertionError("ulaşılamaz")

    def _wait(self) -> None:
        remaining = self._last_request + self.delay - time.monotonic()
        if remaining > 0:
            time.sleep(remaining)
        self._last_request = time.monotonic()
