# Project Status

## Last Updated
2026-06-08

## Repository Summary
The `JournalBot` is a Python-based Telegram orchestrator that acts as a secure gateway to internal home infrastructure services (`food-helper` and `fit-builder`). It provides command-based interactions for meal and workout planning, and image-based analysis for calorie tracking.

## Current Services

### JournalBot (This Service)
- **Purpose**: Telegram API gateway and orchestrator.
- **Responsibilities**: 
    - Handle Telegram updates via long-polling.
    - Enforce security (whitelisting and configurable rate limiting).
    - Route commands to internal services via async HTTP.
    - Format internal service responses (Markdown to HTML) for Telegram compatibility.
- **Dependencies**: 
    - `python-telegram-bot` (v20+)
    - `httpx`
    - `markdown`
- **Exposed Interfaces**: 
    - Outgoing: Telegram Bot API, internal service APIs.
    - Incoming: None.

## Current Functionality

### Security
- **Whitelisting**: Multi-user support via `ALLOWED_USERNAMES` and `ALLOWED_USER_IDS` environment variables.
- **Rate Limiting (Kill Switch)**: Configurable rolling window via `RATE_LIMIT_MAX` (default: 10) and `RATE_LIMIT_WINDOW` (default: 60s). Exceeding the limit triggers `os._exit(1)`.

### Command Handlers
- `/status`: Checks `http://food-helper:8080/actuator/health`.
- `/plan_meal [description]`: POSTs to `food-helper`, propagating `userId`.
- `/plan_workout [description]`: POSTs to `fit-builder`, propagating `userId`.
- `calories: [description]` (Photo caption): Multimodal analysis. Sends base64 image, mime type, description, and `userId` to `food-helper`.

### Response Formatting
- **Formatter Utility**: Custom regex-based conversion from LLM-generated Markdown to Telegram HTML (handling headers, lists, and spacing).

## API Surface (Internal)
As per `openapi.yaml` and `internal_api.py`:
- `GET http://food-helper:8080/actuator/health` -> `{"status": str}`
- `POST http://food-helper:8080/meal/plan` -> `{ "description": str, "userId": str }`
- `POST http://food-helper:8080/meal/calories/calculate` -> `{ "imageBase64": str, "mimeType": str, "userId": str, "mealDescription": str }`
- `POST http://fit-builder:8080/workout/plan` -> `{ "description": str, "userId": str }`

## Architecture Snapshot
- **Pattern**: Orchestrator / API Gateway.
- **Concurrency**: Fully async using `python-telegram-bot` and `httpx`.
- **Security**: Decorator-based interceptors for authorization and rate limiting.

## Planned vs Implemented

### Completed
- All tasks from `plan.md` (TASK-1 to TASK-6).
- Security middleware with whitelist and rate limiting.
- Multimodal calorie calculation (originally beyond MVP scope).
- Specialized Markdown-to-HTML formatting.

### Discrepancies
- None. Implementation perfectly aligns with the current `plan.md`.

## Technical Debt
- **No Automated Tests**: No unit tests for `formatter.py`, `security.py`, or command handlers.
- **Hardcoded Internal URLs**: Downstream service URLs are hardcoded in `internal_api.py`.
- **Error Handling**: Basic catch-all in `errors.py`; HTTP status error parsing is centralized but could be more robust.
- **Configuration**: `config.py` relies on raw `os.environ` without structured validation (e.g., Pydantic).

## Recommended Next Steps
1. **Infrastructure**: Parameterize downstream URLs in `.env`.
2. **Quality**: Add unit tests for the HTML formatter and security logic.
3. **Resilience**: Implement retries for internal API calls.
4. **Validation**: Use Pydantic for configuration and API request/response models.
