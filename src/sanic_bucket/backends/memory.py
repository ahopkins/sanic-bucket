from typing import Dict
from sanic_bucket.backends.base import BaseBackend
from sanic import Sanic
from sanic_bucket.bucket import TokenBucket


class InMemoryBackend(BaseBackend):
    async def _setup(self, app: Sanic) -> None:
        self.cache: Dict[str, TokenBucket] = {}

    async def create(self, ident: str) -> TokenBucket:
        bucket = TokenBucket(ident)
        self.cache[ident] = bucket
        return bucket

    async def persist(self, bucket: TokenBucket) -> None:
        ...

    async def fetch(self, ident: str) -> TokenBucket:
        bucket = self.cache.get(ident)
        if not bucket:
            bucket = await self.create(ident=ident)

        return bucket
