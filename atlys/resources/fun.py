"""Fun endpoints: quotes, jokes, pantun, fun facts."""


class Fun:
    def __init__(self, client):
        self._c = client

    def quote_random(self):
        """A random inspirational quote."""
        return self._c.get("/v1/fun/quote-random")

    def jokes(self):
        """A random joke (Indonesian)."""
        return self._c.get("/v1/fun/jokes")

    def pantun(self):
        """A random Indonesian pantun."""
        return self._c.get("/v1/fun/pantun")

    def fakta_unik(self):
        """A random fun fact."""
        return self._c.get("/v1/fun/fakta-unik")
