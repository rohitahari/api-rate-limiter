from fastapi import Request, HTTPException
import time

RATE_LIMIT_IP = 10
RATE_LIMIT_API = 50
WINDOW = 60

async def rate_limiter(request: Request):

    api_key = request.headers.get("X-API-Key")
    client_ip = request.client.host

    # If API key exists → use API key rate limit
    if api_key:
        key = f"rate_limit_api:{api_key}"
        limit = RATE_LIMIT_API
        error_message = "API key rate limit exceeded"

    else:
        key = f"rate_limit_ip:{client_ip}"
        limit = RATE_LIMIT_IP
        error_message = "IP rate limit exceeded"

    count = redis_client.get(key)

    if count and int(count) >= limit:
        raise HTTPException(status_code=429, detail=error_message)

    redis_client.incr(key)

    if not count:
        redis_client.expire(key, WINDOW)
