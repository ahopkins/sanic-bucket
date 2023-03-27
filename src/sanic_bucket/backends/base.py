from abc import ABC, abstractmethod
from sanic import Sanic
from sanic_bucket.bucket import TokenBucket


class BaseBackend(ABC):
    @abstractmethod
    async def create(self, ident: str) -> TokenBucket:
        """Create a token bucket"""

    @abstractmethod
    async def fetch(self, ident: str) -> TokenBucket:
        """Retrieve a token bucket"""

    @abstractmethod
    async def persist(self, bucket: TokenBucket) -> None:
        """Persist a token bucket"""

    def startup(self, app: Sanic) -> None:
        app.before_server_start(self._setup)
        app.after_server_stop(self._teardown)

    async def _setup(self, app: Sanic) -> None:
        ...

    async def _teardown(self, app: Sanic) -> None:
        ...
