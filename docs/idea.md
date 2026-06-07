# Project: Telegram Orchestrator Bot
**Objective:** Serve as the sole secure, user-facing interface for the home infrastructure.
**Core Concept:** A Python-based Telegram bot using long-polling to fetch commands securely from Telegram's cloud. It acts as an API gateway/orchestrator, intercepting user commands, validating authorization, and routing traffic to internal Docker services.
**MVP Scope:**
- Three commands: `/plan_meal [description]`, `/plan_workout [description]`, `/status`.
- Image analysis: Send a photo with "calories: [description]" to get nutritional analysis.
- Security mechanisms: Strict Whitelisting (Username + User ID) and an aggressive kill-switch rate limiter (>10 requests/minute triggers application shutdown).
- Output: Parses JSON from downstream services and returns the `result` string formatted as HTML to the user.