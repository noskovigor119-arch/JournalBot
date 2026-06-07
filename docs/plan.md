# Implementation Plan: Orchestrator Bot

- [x] **TASK-1: Project Setup & Dependencies**
  Create `requirements.txt` (`python-telegram-bot`, `httpx`). Initialize basic `main.py` with standard logging setup.
- [x] **TASK-2: Security Middleware (Whitelist & Rate Limiter)**
  Implement a decorator or global middleware that first checks `ALLOWED_USERNAME` and `ALLOWED_USER_ID`. Implement the 60-second rolling window using a Python `deque`. Trigger `os._exit(1)` upon limit breach.
- [x] **TASK-3: Internal HTTP Client Integration**
  Set up an async `httpx.AsyncClient` wrapper with timeouts to communicate over the Docker bridge network.
- [x] **TASK-4: Command Logic**
  Implement `/status`, `/plan_meal`, and `/plan_workout`. Handle empty descriptions by passing a default string (e.g., "Standard default plan"). Parse `{ "result": "..." }` JSON responses.
- [x] **TASK-5: Containerization**
  Write a `Dockerfile` using `python:3.11-slim`. Ensure `python main.py` is the entrypoint. Do not expose any ports.
- [x] **TASK-6: Image Analysis (Calories Calculation)**
  Implement image handling for photos with "calories:" caption. Forward base64 image and description to `food-helper`. Parse and format the result.