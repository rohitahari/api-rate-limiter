from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
from app.redis_client import redis_client

IP_RATE_LIMIT = 10
API_KEY_RATE_LIMIT = 50
WINDOW = 60


class RateLimiterMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        client_ip = request.client.host
        api_key = request.headers.get("X-API-Key")

        ip_key = f"rate_limit_ip:{client_ip}"
        api_key_key = f"rate_limit_api:{api_key}" if api_key else None

        # ---- IP RATE LIMIT ----
        ip_count = redis_client.get(ip_key)

        if ip_count is None:
            redis_client.set(ip_key, 1, ex=WINDOW)
        elif int(ip_count) >= IP_RATE_LIMIT:
            return JSONResponse(
                status_code=429,
                content={"detail": "IP rate limit exceeded"},
            )
        else:
            redis_client.incr(ip_key)

        # ---- API KEY RATE LIMIT ----
        if api_key:

            api_count = redis_client.get(api_key_key)

            if api_count is None:
                redis_client.set(api_key_key, 1, ex=WINDOW)
            elif int(api_count) >= API_KEY_RATE_LIMIT:
                return JSONResponse(
                    status_code=429,
                    content={"detail": "API key rate limit exceeded"},
                )
            else:
                redis_client.incr(api_key_key)

        response = await call_next(request)

        return response


