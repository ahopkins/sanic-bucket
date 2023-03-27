from inspect import isawaitable
from functools import wraps
from sanic import Request
from sanic_bucket.limiter import BucketLimiter


def ratelimit(rate: int):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request: Request, *args, **kwargs):
            limiter: BucketLimiter = request.app.ctx.bucket_limiter

            await limiter.handle(request)

            response = f(request, *args, **kwargs)
            if isawaitable(response):
                response = await response

            return response

        return decorated_function

    return decorator
