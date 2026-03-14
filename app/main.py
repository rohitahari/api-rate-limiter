from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import redis

app = FastAPI()

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

RATE_LIMIT_IP = 10
RATE_LIMIT_API = 50
WINDOW = 60


@app.middleware("http")
async def rate_limiter(request: Request, call_next):

    api_key = request.headers.get("X-API-Key")
    client_ip = request.client.host

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
        return JSONResponse(
            status_code=429,
            content={"detail": error_message}
        )

    redis_client.incr(key)

    if not count:
        redis_client.expire(key, WINDOW)

    response = await call_next(request)
    return response


@app.get("/")
def home():
    return {"message": "Request allowed"}

