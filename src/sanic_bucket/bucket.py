from asyncio import BoundedSemaphore
from math import floor
from time import time

from sanic_bucket.exceptions import TooManyRequests


class TokenBucket:
    __slots__ = ("ident", "checkin", "tokens", "_tokens", "refill_interval")

    def __init__(
        self, ident: str, max_size: int = 3, refill_interval: float = 1.0
    ):
        self.ident = ident
        self.checkin = time()
        self.refill_interval = refill_interval
        self.tokens = BoundedSemaphore(max_size)

    def __str__(self) -> str:
        un = "" if self.tokens.locked() else "un"
        tokens = f"[{un}locked, {self.tokens._value}]"
        return f"<TokenBucket ident={self.ident} tokens={tokens}>"

    def __repr__(self) -> str:
        return str(self)

    async def consume(self) -> None:
        current = time()
        time_passed = current - self.checkin
        self.checkin = current

        calculated = floor(time_passed / self.refill_interval)
        for _ in range(calculated):
            try:
                self.tokens.release()
            except ValueError:
                break

        if self.tokens.locked():
            raise TooManyRequests

        await self.tokens.acquire()

    @property
    def size(self) -> int:
        return self.tokens._value
