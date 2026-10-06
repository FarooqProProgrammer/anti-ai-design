# Architecture & conventions — <project>

> Gate-3 reviewers enforce this file literally. Keep it short, concrete, and true to the codebase.
> `/spiral-init` drafts it from the code; the tech lead owns it. Point to example files instead of describing at length.

## Stack
- <framework + version>, <language>, <state/data library>, <styling>, <test runner>

## Structure
- Features live in `<path>/<feature>/` with `<files>`. Example: `<path to a good existing feature>`
- Shared UI components: `<path>`. Reuse before creating; new shared components need a reason.
- API/data access only through `<layer>`. Components never call `fetch` directly.

## Rules
1. <e.g. Server state via TanStack Query hooks in `hooks/`; no data fetching in components.>
2. <e.g. Forms: react-hook-form + zod schema in `schema.ts` beside the form.>
3. <e.g. Styling: Tailwind tokens from the theme only; no hex values or arbitrary px in components.>
4. <e.g. Errors: user-facing errors go through `toastError()`; never swallow exceptions.>
5. <e.g. Naming: components PascalCase, hooks `useX`, files kebab-case.>
6. Accessibility: interactive elements are buttons or links with accessible names; images have alt text.
7. No new dependencies without saying why in the checkpoint's gate-3 response.

## Testing
- <runner>, tests in `<dir>`. Prefer integration tests that render the screen with mocked network (`<msw/nock>`).
- No snapshot tests. No testing implementation details (internal state, private functions).

## Never
- Commit secrets, `.env` values, or real client data in fixtures.
- Disable lint rules or type checks inline (`eslint-disable`, `@ts-ignore`, `any`) without a comment justifying it.
