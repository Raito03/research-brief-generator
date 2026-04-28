# Production Testing Specification: AI Research Brief Generator

## 1. Project Overview
The AI Research Brief Generator is a production-ready research assistant that utilizes FastAPI on the backend to orchestrate LangGraph nodes, paired with a Next.js (React 19) frontend that consumes Server-Sent Events (SSE) to render a streaming editorial UI.

This document serves as the foundational **Product Requirements Document (PRD)** for TestSprite and any other automated testing platforms evaluating the repository.

## 2. Architecture & Components

### 2.1 Backend (FastAPI + LangGraph)
- **Primary Entrypoint:** `app/api.py` exposes REST endpoints (`/health`, `/brief`, `/brief/stream`).
- **Orchestration:** `app/advanced_workflow.py` compiles a LangGraph `StateGraph` consisting of planning, search, summarization, and synthesis nodes.
- **Data Schemas:** `app/schemas.py` defines strict Pydantic inputs (`BriefRequest`) and outputs (`FinalBrief`).
- **LLM Abstraction:** `app/llm_providers.py` handles model instantiation, gracefully falling back from Google Gemini to Cloudflare Workers AI to OpenRouter on quota exhaustion.
- **Deep Extraction:** `app/crawler.py` uses `crawl4ai` (Playwright-backed) to fetch full Markdown pages from URLs discovered by the `ddgs` (DuckDuckGo Search) module.
- **Streaming Context:** State and logs are safely isolated across concurrent requests using Python `contextvars` (`request_log_callback` and `model_name_ctx`).

### 2.2 Frontend (Next.js + Tailwind CSS)
- **Primary Framework:** Next.js 16.2 with Turbopack, React 19, and Tailwind CSS v4.
- **Design Philosophy:** Premium, continuous-scroll "editorial" layout utilizing typography-led hierarchy (Playfair Display / Inter) instead of generic card mosaics.
- **State Management:** `app/page.tsx` uses a centralized `ChatInterface` to transition through `'idle' | 'loading' | 'result' | 'error'` states.
- **SSE Integration:** `lib/api.ts` defines an async generator (`streamResearchBrief`) that reads the chunked HTTP stream and decodes it in real-time.

## 3. Core Testing Scenarios (Acceptance Criteria)

### 3.1 Backend API Tests
- **T1: Health Check:** GET `/health` must return `{"status": "healthy"}` within 100ms.
- **T2: Input Validation:** POST `/brief` with a topic `< 5` characters must return HTTP 422 Unprocessable Entity.
- **T3: Async Concurrency:** `generate_brief` must utilize `asyncio.to_thread(workflow_app.invoke)` to prevent blocking the global event loop. Test tools should send 5 parallel requests and verify they stream simultaneously without latency spikes.
- **T4: LLM Fallback:** If `GOOGLE_API_KEY` is mocked to throw a `ResourceExhausted` error, the workflow must catch it and instantly route the request to the next configured provider in `app/llm_providers.py`.
- **T5: Crawler Resilience:** `fetch_page_content(url)` must catch HTTP timeouts and return a gracefully degraded fallback string rather than crashing the summarization node.

### 3.2 Frontend End-to-End Tests
- **T6: Parameter Collection:** The user must be able to input a topic, select a depth (1-5), and choose a summary length (100-1000) using keyboard navigation (Enter key progression) in `ParameterCollection.tsx`.
- **T7: SSE Parsing:** When the backend emits `{"type": "log", "message": "Planning..."}`, the `LoadingDisplay` component must render the exact text in a fading animation without duplicating prior log lines.
- **T8: Editorial Rendering:** When `{"type": "result", "data": {...}}` is received, `ResultDisplay.tsx` must parse the Pydantic JSON and render the `executive_summary`, `key_findings`, and `detailed_analysis` continuously without requiring the user to click any "accordion" or expansion buttons.

## 4. Known Gaps & Future Implementation
*These are documented areas that are currently mocked or incomplete. Tests targeting these features should expect failure or mock stubs.*

1. **Follow-Up Memory:** The `follow_up: bool` parameter in `BriefRequest` is parsed but the backend does not currently hook into a real persistence layer (e.g., Vector DB) to retrieve past session briefs.
2. **LangSmith Telemetry:** The `langsmith_integration.py` hook exists in the codebase but is not fully wrapped around the production endpoints.
3. **Authentication:** The API relies solely on CORS (which requires environment-specific domain pinning before production) and currently lacks JWT or API key middleware.

## 5. Test Environment Prerequisites
- Python 3.11+
- Playwright Chromium binaries (`python -m playwright install chromium`)
- API Keys provided via `.env` or system environment for at least one active LLM provider.