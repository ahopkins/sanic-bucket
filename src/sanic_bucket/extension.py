from typing import Callable, Optional
from sanic import Request
from sanic_bucket.limiter import BucketLimiter
from sanic_ext import Extend, Extension
from sanic_bucket.backends.base import BaseBackend
from sanic_bucket.backends.memory import InMemoryBackend
from sanic_bucket.identify import identify_by_remote_addr


class BucketExtension(Extension):
    name = "bucket"

    def __init__(
        self,
        backend: Optional[BaseBackend] = None,
        identify: Callable[[Request], str] = identify_by_remote_addr,
    ):
        if not backend:
            backend = InMemoryBackend()
        self.limiter = BucketLimiter(backend=backend, identify=identify)

    def startup(self, bootstrap: Extend) -> None:
        self.limiter.startup(self.app)
