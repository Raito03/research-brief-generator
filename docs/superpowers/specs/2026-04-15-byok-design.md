# BYOK for Research Brief Generation

## Goal

Add Bring Your Own Key (BYOK) to research brief generation so a user can optionally provide provider credentials for the current request flow, while preserving the existing FastAPI backend, LangGraph workflow, Next.js frontend, and SSE streaming UX.

v1 is hybrid-ready and request-scoped:
- BYOK is optional per submitted request.
- No server-side persistence is introduced.
- Future browser persistence may be added later without changing the backend request contract, but the client must still send `byok` on any request that should use it.
- The backend remains the only component that talks to model providers.

## Non-Goals

- No server-side storage of user credentials.
- No account-level key management or settings dashboard.
- No frontend-to-provider direct calls.
- No silent fallback to app-managed or cross-provider credentials when a selected BYOK credential fails.
- No change to the existing app-managed fallback behavior for requests that do not use BYOK.

## Current Context

The current stack already routes all research brief generation through:
- **Next.js frontend** with SSE client handling in `frontend/lib/api.ts`
- **FastAPI backend** in `app/api.py`
- **LangGraph workflow** in `app/advanced_workflow.py`
- **Provider resolution** in `app/llm_providers.py`

Current impacted files:
- `frontend/lib/api.ts`
- `frontend/components/ParameterCollection.tsx`
- `frontend/components/ChatInterface.tsx`
- `frontend/types/index.ts`
- `app/api.py`
- `app/schemas.py`
- `app/advanced_workflow.py`
- `app/llm_providers.py`

Current request flow:
1. `ChatInterface.tsx` builds the research request.
2. `frontend/lib/api.ts` posts JSON to `POST /brief/stream`.
3. `app/api.py` creates initial workflow state and starts SSE streaming.
4. `app/advanced_workflow.py` invokes provider creation in multiple nodes.
5. `app/llm_providers.py` resolves credentials using the app-managed provider chain.

This means BYOK must enter at the API boundary and remain request-scoped across the full workflow so concurrent requests cannot leak credentials into each other.

## Proposed Architecture

Introduce an optional **request-scoped BYOK envelope** on the existing research brief request.

Design principles:
- The frontend only collects and forwards the optional BYOK payload.
- The backend validates, scopes, and uses the credentials.
- Raw BYOK credentials are never persisted server-side and are never written to workflow outputs, logs, or returned SSE payloads.
- Provider selection is resolved per request, not from global mutable state.
- BYOK applies only to the submitted request; later requests use BYOK only if the client explicitly sends `byok` again.

Architecture shape:
- `frontend/types/index.ts` extends the request and form types with an optional BYOK object.
- `frontend/components/ParameterCollection.tsx` exposes BYOK as an advanced inline option during the request flow.
- `frontend/components/ChatInterface.tsx` keeps BYOK only in in-memory component state for the current interaction; later requests use it only if the client includes `byok` again.
- `app/schemas.py` defines the canonical BYOK request schema; `app/api.py` should consume that shared schema rather than maintaining a divergent local copy.
- `app/api.py` installs request-scoped provider config before invoking the LangGraph workflow.
- `app/llm_providers.py` resolves credentials per request. If `byok.enabled` is true, it uses only the selected user-provided credential for the selected provider. If BYOK is absent or disabled, it uses the existing app-managed provider chain.
- If BYOK is explicitly selected and the supplied credential fails validation, authentication, quota, or provider config checks, the request hard-fails and does not continue to app-managed or cross-provider credentials.
- `app/advanced_workflow.py` must propagate typed BYOK/provider failures as terminal request failures instead of producing fallback content.

## Request Contract

The existing `/brief` and `/brief/stream` request body remains the same shape, with one optional field added:

```json
{
  "topic": "artificial intelligence in healthcare",
  "depth": 3,
  "user_id": "user_1713200000000",
  "summary_length": 300,
  "follow_up": false,
  "byok": {
    "enabled": true,
    "provider": "google",
    "credentials": {
      "api_key": "user-supplied-secret"
    }
  }
}
```

Contract rules:
- `byok` is optional.
- If `byok` is absent or `enabled` is false, behavior remains app-managed.
- `provider` is required when `byok.enabled` is true.
- `credentials` is required when `byok.enabled` is true.
- BYOK applies only to the submitted request. A later request uses BYOK only if the client explicitly sends `byok` again.
- The contract is source-agnostic: the backend does not care whether the frontend got the credential from manual entry in v1 or browser persistence later.
- The backend request contract is therefore stable for future browser-side persistence.

## Frontend UX

BYOK is presented as an **advanced option** inside the existing request flow, not a separate settings surface.

UX behavior:
- Add a collapsed advanced section in `frontend/components/ParameterCollection.tsx`, ideally on the confirmation step where the user already reviews topic, depth, and summary length.
- The section offers:
  - toggle: “Use my own provider key”
  - provider selector
  - credential input field(s) appropriate to the selected provider
- Keep the default path unchanged for users who do not expand the advanced option.
- Do not introduce account preferences, saved profiles, or a dashboard.

Frontend state changes:
- `frontend/types/index.ts` adds BYOK-related types to `BriefRequest` and `FormData`.
- `frontend/components/ChatInterface.tsx` includes the BYOK payload when building the request sent to `streamResearchBrief`.
- `frontend/lib/api.ts` continues posting to `/brief/stream` and does not change transport behavior beyond sending the extended JSON body.

Error UX:
- If BYOK is selected and the key fails, the existing error state in `ChatInterface.tsx` should show a direct credential/provider error.
- The UI should not imply that the app silently retried with another credential.

## Backend Changes

### `app/schemas.py`
- Add canonical BYOK request models, including provider enum/type and credentials envelope.
- Make `BriefRequest` the single shared request schema for BYOK-capable endpoints.

### `app/api.py`
- Replace or align the local `BriefRequest` definition with the shared schema from `app/schemas.py`.
- Validate the optional BYOK payload at request entry.
- Set request-scoped provider config for the lifetime of the workflow execution and reset it after completion.
- Do not carry BYOK forward to later requests unless the client sends `byok` again.
- Preserve SSE transport, but return typed BYOK failures as explicit `error` events.

### `app/llm_providers.py`
- Add a request-scoped provider context object.
- Extend provider resolution so it can choose credentials based on the current request.
- Enforce credential selection as:
  1. if BYOK is active, use only the selected user-provided credential for the selected provider
  2. if BYOK is absent or disabled, use the existing app-managed credential and cross-provider fallback chain
- When BYOK is active and the supplied credential fails validation, authentication, quota, or provider config checks, raise a typed terminal error and do not continue to app-managed or cross-provider credentials.

### `app/advanced_workflow.py`
- Keep provider access inside the backend workflow.
- Ensure typed BYOK/provider failures stop the workflow and bubble out.
- Do not allow synthesis or fallback-brief generation to mask a BYOK credential failure.

## Security & Error Handling

Security requirements:
- BYOK credentials are request-scoped only.
- No server-side persistence in v1.
- No writing raw credentials into workflow state, logs, analytics, exceptions, or SSE events.
- No reuse of a previous request’s BYOK credential on another request unless the client explicitly re-sends the `byok` object.
- Reset request-scoped provider context after each workflow execution, including failure paths.

Error handling rules:
- Invalid BYOK payload → request validation error.
- Missing required BYOK fields when enabled → request validation error.
- Provider validation/authentication/quota/config failure for a selected BYOK credential → hard-fail that request with no app-managed or cross-provider fallback.
- Non-BYOK requests keep the current app-managed fallback behavior.
- SSE should emit a clear terminal error event for BYOK failures and stop streaming further model work.

## Testing Strategy

Cover the feature at three levels:

1. **Schema and contract tests**
   - valid request without BYOK still passes
   - valid request with BYOK passes
   - invalid BYOK payloads fail validation
   - a later request without `byok` does not inherit a prior request’s BYOK settings

2. **Provider resolution tests**
   - when BYOK is active, only the selected user-provided credential is used
   - app-managed credential is used when BYOK is absent
   - existing fallback chain still works for non-BYOK requests
   - BYOK failure hard-fails and does not continue to app-managed or cross-provider credentials

3. **Request isolation and SSE integration tests**
   - two concurrent requests with different BYOK values do not leak credentials across requests
   - `/brief/stream` emits normal logs/results for success cases
   - `/brief/stream` emits terminal `error` for BYOK failures
   - frontend receives and renders BYOK errors through the existing error state

## Acceptance Criteria

- A user can optionally provide provider credentials for the current research brief request flow.
- BYOK is exposed as an advanced inline option in the frontend, not a settings dashboard.
- The backend is the only component that talks to model providers.
- The request contract supports future browser persistence without requiring contract changes.
- BYOK is request-scoped and safe under concurrent requests.
- When BYOK is present and enabled, only the selected user-provided credential is used for that request.
- If BYOK is selected and the provided credential fails validation, authentication, quota, or provider config checks, the request hard-fails with no app-managed or cross-provider fallback.
- BYOK applies to one submitted request only unless the client explicitly re-sends the same `byok` object on a later request.
- Existing non-BYOK requests preserve current behavior.

## Open Questions

No blocking product questions remain for v1. The only intentionally deferred area is browser-side persistence; when added later, it must populate the same `byok` request shape on each request and remain client-only so the backend contract and security model do not change.
