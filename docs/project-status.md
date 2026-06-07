# Project Status

## Last Updated
2026-06-06

## Repository Summary
The `JournalBot` is a Python-based Telegram orchestrator that acts as a secure gateway to internal home infrastructure services (`food-helper` and `fit-builder`). It provides command-based interactions for meal and workout planning, and image-based analysis for calorie tracking.

## Current Services

### JournalBot (This Service)
- **Purpose**: Telegram API gateway and orchestrator.
- **Responsibilities**: 
    - Handle Telegram updates via long-polling.
    - Enforce security (whitelisting and rate limiting).
    - Route commands to internal services.
    - Format internal service responses (Markdown to HTML) for Telegram.
- **Dependencies**: 
    - `python-telegram-bot`
    - `httpx`
    - `markdown`
- **Exposed Interfaces**: Telegram Bot API (outgoing), No incoming ports.

## Current Functionality

### Security
- **Whitelisting**: Only users in `ALLOWED_USERNAMES` and `ALLOWED_USER_IDS` can interact with the bot.
- **Rate Limiting (Kill Switch)**: If more than 10 requests are received within 60 seconds, the application terminates (`os._exit(1)`).

### Command Handlers
- `/status`: Checks health of `food-helper`.
- `/plan_meal [description]`: Sends meal planning request to `food-helper`. Includes `userId`.
- `/plan_workout [description]`: Sends workout planning request to `fit-builder`.
- `calories: [description]` (Photo caption): Sends photo and description to `food-helper` for nutritional analysis.

### Response Formatting
- Converts Markdown responses from internal services to Telegram-compatible HTML using a custom formatter.

## API Surface

### Internal API Client (`internal_api.py`)
- `GET http://food-helper:8080/actuator/health`
- `POST http://food-helper:8080/meal/plan` -> `{ "description": str, "userId": str }`
- `POST http://food-helper:8080/meal/calories/calculate` -> `{ "imageBase64": str, "mimeType": str, "userId": str, "mealDescription": str }`
- `POST http://fit-builder:8080/workout/plan` -> `{ "description": str }`

## Architecture Snapshot
The bot follows an orchestrator pattern. It uses async handlers and an async HTTP client (`httpx`) to communicate with downstream microservices. Security is implemented via decorators that intercept every request.

## Planned vs Implemented

### Completed
- Project setup and dependencies.
- Security middleware (Whitelist & Rate Limiter).
- Internal HTTP client integration.
- Core commands (`/status`, `/plan_meal`, `/plan_workout`).
- Containerization (Dockerfile).
- Image analysis for calories calculation (originally beyond MVP scope).
- Markdown-to-HTML formatting for Telegram.

### Partially Implemented
- None detected.

### Not Implemented
- None detected.

### Implemented Beyond Original Plan
- **Calorie Calculation**: Multimodal support (image + text) for food analysis.
- **HTML Formatting**: Specialized utility to handle LLM-generated Markdown in Telegram.
- **Pluralized Security Config**: Support for multiple allowed users via comma-separated env vars.

## Git History Summary
- **Initial Phase**: MVP setup with basic commands and security.
- **Enhancement Phase**: Added `userId` propagation and HTML formatting to improve user experience and traceability.
- **Expansion Phase**: Introduced multimodal capabilities (image analysis for calories) and refined the regex-based command triggering for captions.
- **Refinement Phase**: Improved error handling for API calls.

## Technical Debt
- **Error Handling**: While basic error handling exists, more granular error messages for different HTTP failure modes could be improved.
- **Tests**: No automated tests (unit or integration) were found in the repository.
- **Config Validation**: `config.py` raises `ValueError` but does not provide a graceful way to handle missing env vars before startup (it happens at runtime when called).
- **Hardcoded URLs**: Service URLs are hardcoded in `internal_api.py` instead of being configurable via environment variables.

## Recommended Next Steps
1. **Configurability**: Move downstream service URLs to environment variables.
2. **Testing**: Implement unit tests for `formatter.py` and `security.py`.
3. **Robustness**: Add retry logic for internal API calls using `httpx`.
4. **Validation**: Use Pydantic for configuration and internal API models.
