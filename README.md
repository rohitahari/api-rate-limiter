# FastAPI Redis Rate Limiter

A simple API rate limiting system built using FastAPI and Redis.

## Features

- IP-based rate limiting
- API key based rate limiting
- Redis counter storage
- FastAPI middleware implementation

## Tech Stack

- FastAPI
- Redis
- Python

## How It Works

1. Client sends request
2. Middleware checks Redis for request count
3. If limit exceeded → request blocked
4. Otherwise request allowed

## Run Locally

Install dependencies

pip install -r requirements.txt

Start Redis

redis-server

Run server

python -m uvicorn app.main:app --reload --port 8002

Test API

curl http://127.0.0.1:8002
