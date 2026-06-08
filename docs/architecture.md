# Architecture: Telegram Orchestrator Bot

## Tech Stack
- **Language:** Python 3.11+
- **Libraries:** `python-telegram-bot` (v20+ for async), `httpx` (for async internal HTTP requests), `collections.deque` (for rate limiting), `markdown` (for HTML formatting).

## Components
1. **Security Interceptor:** Middleware running before any command logic.
    - **Identity Check:** Compares `update.effective_user.username` and `update.effective_user.id` against environment variables `ALLOWED_USERNAMES` and `ALLOWED_USER_IDS` (comma-separated lists). Yields "Unauthorized" if mismatched.
    - **Rate Limiter (Kill Switch):** A `deque` storing timestamps. If an incoming request pushes the count > `RATE_LIMIT_MAX` within a rolling `RATE_LIMIT_WINDOW` (configured in `.env`), the system invokes `os._exit(1)` to violently terminate the container (acting as a circuit breaker). Default is 10 requests per 60 seconds.
2. **Command Handlers:**
    - `/status`: Checks reachability of `http://food-helper:8080/actuator/health`.
    - `/plan_meal`: Extracts string args. POSTs to `http://food-helper:8080/meal/plan` with `{"description": "...", "userId": "..."}`.
    - `/plan_workout`: Extracts string args. POSTs to `http://fit-builder:8080/workout/plan` with `{"description": "..."}`.
    - `calories` (image caption): Triggered by photos with "calories:" caption. POSTs to `http://food-helper:8080/meal/calories/calculate` with base64 image and description.

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
    ├── handlers/
    │   ├── commands.py    # /status, /plan_meal, /plan_workout, handle_calories
    │   └── errors.py      # Fallback error handlers
    └── utils/
        └── formatter.py   # Markdown to Telegram HTML conversion
```