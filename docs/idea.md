# Project: JournalBot

## Objective
Serve as the sole secure, user-facing gateway and orchestrator for the home AI infrastructure.

## Core Concept
JournalBot is a specialized Telegram-based interface that centralizes access to private home-cloud AI services. It intercepts user commands, validates authorization, and routes traffic to internal LLM-driven services like FoodHelper and FitBuilder. By acting as a secure orchestrator, it provides a seamless natural language interface for managing daily health, nutrition, and fitness habits while ensuring strict infrastructure security and privacy.

## Target Users
- **Owner/Authorized Users:** Individuals managing their personal health and home infrastructure through a familiar chat interface.
- **Home Infrastructure Services:** Downstream microservices that require a secure, centralized way to receive processed user intent and imagery.

## Business Goals
- **Unified Interface:** Provide a single entry point for multiple specialized AI services (nutrition, fitness, etc.).
- **Security & Privacy:** Enforce strict access control to prevent unauthorized use of private AI infrastructure and prevent service abuse via aggressive rate limiting.
- **User Experience:** Transform complex Markdown outputs from internal AI services into beautiful, readable Telegram-compatible formats.

## Core Use Cases
- **Nutrition Orchestration:** Forwarding meal descriptions and food photography to internal services for planning and caloric analysis.
- **Fitness Orchestration:** Routing exercise-related requests to specialized planning services.
- **System Health Monitoring:** Providing a quick way to verify the status and reachability of the internal service mesh.

## Non-Goals
- **Business Logic Ownership:** JournalBot does not generate meal or workout plans itself; it delegates reasoning to downstream services.
- **Public Access:** This is not a public bot; it is explicitly designed for a private, whitelisted set of users.
- **Persistent Data Storage:** The bot does not maintain a database of user history; it acts as a stateless pass-through and formatter.
- **Direct Internet Exposure:** The bot does not expose any incoming ports or public APIs, operating strictly via long-polling.
