from sanic_bucket.backends.base import BaseBackend
from typing import Callable
from sanic import Request, Sanic


class BucketLimiter:
    def __init__(
        self, backend: BaseBackend, identify: Callable[[Request], str]
    ) -> None:
        self.backend = backend
        self.identify = identify

    def startup(self, app: Sanic) -> None:
        app.ctx.bucket_limiter = self
        self.backend.startup(app)

    async def handle(self, request: Request) -> None:
        bucket_ident = self.identify(request)
        bucket = await self.backend.fetch(bucket_ident)
        await bucket.consume()
        await self.backend.persist(bucket)
