# Expected Agent Output

## Mode

Clarify and scaffold.

## Confirmed

- The user wants a browser extension.
- The extension should collect useful snippets from web pages.
- Implementation should not start until the first loop is defined.

## Assumptions

- MVP target: save selected text, source URL, page title, and timestamp.
- First storage target: local extension storage, not a remote database.
- First user: the requester, using one browser profile.

## Open Questions

- Which browser should be first: Chrome, Edge, or Firefox?
- Should snippets be searchable in v1?
- Should export be required in the first loop?

## First Loop

Build only a requirements and proof-of-shape loop:

- Create state files.
- Define the MVP snippet record.
- Define acceptance criteria for saving one selected snippet.
- Do not write extension code yet.

## Acceptance Criteria

- `state/triage.md` contains the current goal, scope, and priority queue.
- `state/decisions.md` records the MVP default assumptions.
- `state/inbox.md` records questions requiring user judgment.
- `state/next.md` defines the next executable loop and verification method.

## Verification

PASS if all state files exist and the next loop can be started without
reconstructing context from chat.
