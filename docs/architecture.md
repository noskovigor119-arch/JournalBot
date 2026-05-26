# Architecture: Telegram Orchestrator Bot

## Tech Stack
- **Language:** Python 3.11+
- **Libraries:** `python-telegram-bot` (v20+ for async), `httpx` (for async internal HTTP requests), `collections.deque` (for rate limiting).

## Components
1. **Security Interceptor:** Middleware running before any command logic.
    - **Identity Check:** Compares `update.effective_user.username` and `update.effective_user.id` against environment variables `ALLOWED_USERNAME` and `ALLOWED_USER_ID`. Yields "Unauthorized" if mismatched.
    - **Rate Limiter (Kill Switch):** A `deque` storing timestamps. If an incoming request pushes the count > 10 within a rolling 60-second window, the system invokes `os._exit(1)` to violently terminate the container (acting as a circuit breaker).
2. **Command Handlers:**
    - `/status`: Checks reachability of `http://food-helper:8080/actuator/health` (or basic ping).
    - `/plan_meal`: Extracts string args. POSTs to `http://food-helper:8080/meal/plan` with `{"description": "..."}`. Extracts `result` from response.
    - `/plan_workout`: Extracts string args. POSTs to `http://fit-builder:8080/workout/plan` with `{"description": "..."}`. Extracts `result` from response.

## Network & Deployment constraints
- Must run in Docker. No port exposure. Resolves internal DNS (e.g., `food-helper`, `fit-builder`).

```
JournalBot/
├── Dockerfile
├── requirements.txt
├── .env.example
└── src/
├── __init__.py
├── main.py
├── config.py          # Loads and validates env vars
├── security.py        # Whitelisting and rate-limiting logic
├── clients/
│   └── internal_api.py # HTTPX client for FoodHelper and FitBuilder
└── handlers/
├── commands.py    # /status, /plan_meal, /plan_workout
└── errors.py      # Fallback error handlers
```