# Chat context and empty-response fix

This patch addresses the case where Failure Detective AI receives a follow-up message but responds as though it has no context, or displays the generic “I couldn't produce a response. Please rephrase the problem.” message.

## Changes

- The chat API now compares browser-supplied conversation history with Supabase history and uses the longer valid history. An empty or stale persistent-memory read can no longer silently replace context already present in the chat UI.
- The sensor-assisted investigation endpoint applies the same context-preservation rule.
- History trimming now prioritises the newest messages. Previously, an oversized older message could cause the history loop to stop before including newer user details.
- If the hosted model returns an empty message, the backend retries once without tool calling while retaining the latest user message and conversation context.
- If the retry is also empty, the user receives a useful error response that includes the problem description and confirms that earlier details need not be re-entered.
- Added regression tests for preserving the latest context and chronological message order.

## Deployment

Replace the corresponding project files with this package, commit and push through GitHub Desktop, then allow Render to redeploy the backend. The frontend does not require a separate environment-variable change for this patch.

## Validation

Backend test suite: 23 tests passed locally. This does not verify the live Render deployment or Groq provider behaviour.
