# House rules

> Company-wide Spiral rules, read at the start of every checkpoint in **every** client project and enforced by the gate-3
> reviewers. Rules come from project memories through `/spiral-promote` and need a lead's approval (via a PR to the
> toolkit repo). Precedence when rules conflict: project `memory.md` > project `architecture.md` > this file.
>
> **Confidentiality:** rules here travel to every client. Never include client names, domains, product names, URLs,
> data, credentials, or anything traceable to a specific client. Write the generalised lesson only.
>
> Format: one rule per bullet, then `(promoted YYYY-MM-DD, seen in N projects)`.

## Code
- No secrets, tokens, or `.env` values in code, fixtures, logs, or screenshots. (seed)
- Money is handled as integer minor units (or a decimal type), never as floats, and is formatted through one shared helper. (seed)

## UI & taste
- Every list or collection screen has designed loading, empty, and error states; never a blank screen. (seed)
- Interactive elements are real buttons or links with accessible names; touch targets are at least 44×44px on mobile. (seed)

## Tests
- Tests assert on what the user sees or what the caller receives, not on internal state or private functions. (seed)

## Process
- A checkpoint touches one screen or one module; anything more is split. (seed)
