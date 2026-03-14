# API Rate Limiter

A rate limiting system implemented as FastAPI middleware using Redis.

This system protects APIs from abuse by limiting how many requests a client can make within a specific time window.

---

## Features

• IP based rate limiting  
• API key based rate limiting  
• Redis backed request counters  
• FastAPI middleware implementation  
• configurable request limits  

---

## Tech Stack

Python  
FastAPI  
Redis  

---

## System Architecture

Client → FastAPI Server → Rate Limiting Middleware → Redis Counter

Flow

1. Client sends request  
2. Middleware checks request counter in Redis  
3. If request count exceeds limit → request blocked  
4. Otherwise request allowed  

---

## Project Structure

app/
- main.py

requirements.txt  
README.md  

---

## Run Locally

Install dependencies

pip install -r requirements.txt

Start Redis

redis-server

Run API

python -m uvicorn app.main:app --reload --port 8002

---

## Example Request

curl http://127.0.0.1:8002

Response

{
"message": "Request allowed"
}

If rate limit exceeded

{
"detail": "IP rate limit exceeded"
}

---

## Future Improvements

• sliding window rate limiting  
• distributed rate limiting  
• user specific rate limits  
• API analytics

