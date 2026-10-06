# spiral.config.json

Lives at the target project root. `/spiral-init` writes it from the detected stack; engineers edit it by hand.
Every command is run from the project root. Leave a command `null` if the project has no equivalent. Gate 1 then
relies on what remains, and `/spiral-init` warns about it.

```jsonc
{
  "project": "care-platform",
  "stack": "nextjs",                 // free text, for the agents' context
  "autonomy": "checkpoint",          // "checkpoint" | "batch"  (see SKILL.md → Autonomy)
  "commitRunLogs": true,             // commit .spiral/runs/** with each checkpoint
  "branchPrefix": "spiral/",

  "commands": {
    "install":   "pnpm install",
    "typecheck": "pnpm tsc --noEmit",
    "lint":      "pnpm eslint . --max-warnings=0",
    "lintFile":  "pnpm eslint --max-warnings=0 {file}", // run by the quick-check hook after every edit; keep it fast (<10s)
    "test":      "pnpm vitest run",             // whole suite
    "testFile":  "pnpm vitest run {file}",      // single file; {file} is substituted
    "build":     "pnpm build",                  // optional, run at the end of a target
    "dev":       "pnpm dev",                    // started in background for screenshots
    "devUrl":    "http://localhost:3000"
  },

  "tests": {
    "dir": "tests/spiral",            // where spiral-test-writer puts new tests (or "colocated")
    "style": "vitest + @testing-library/react; integration over unit; no snapshot tests"
  },

  "ui": {
    "enabled": true,
    "capture": "playwright",         // "playwright" | "command" | "manual"
    "captureCommand": null,          // for "command": must write PNGs into {outDir}; e.g. simulator/emulator scripts below
    "viewports": [{ "name": "mobile", "width": 390, "height": 844 }, { "name": "desktop", "width": 1440, "height": 900 }],
    "reference": "figma",            // "figma" | "images" | "legacy-app" | "before"
    "referenceDir": ".spiral/reference",  // for "images"
    "legacyUrl": null,               // for "legacy-app" on web
    "reviewer": "claude"             // "claude" (vision subagent) | "gemini" (needs the gemini CLI + GEMINI_API_KEY)
  },

  "gates": {
    "maxAttempts": 5,
    "reviewers": ["architecture", "correctness"],
    "uiBlockingSeverities": ["blocker", "major"]
  },

  "houseRules": null,                // path to the company house-rules.md; null = house/house-rules.md in the spiral skill dir

  "guard": {
    "protected": ["src/generated/**"],   // extra globs the implementer may not edit during a run (added to the built-in list)
    "lintExtensions": null               // file extensions quick-check lints; null = common source extensions
  }
}
```

The file Spiral writes must be **plain JSON** (the comments above are documentation only; the hooks tolerate them, but other
tools may not).

## Installing the hooks

Spiral's guardrails are hooks (`.claude/hooks/spiral/*.mjs`, Node 18+, no dependencies). Install one of two ways:

- **Per project:** copy the toolkit's `.claude/hooks/spiral/` into the project and merge the toolkit's `.claude/settings.json`
  `hooks` block into the project's `.claude/settings.json` (commands use `$CLAUDE_PROJECT_DIR/.claude/hooks/spiral/…`).
- **User-wide:** copy `hooks/spiral/` to `~/.claude/hooks/spiral/` and add the same `hooks` block to `~/.claude/settings.json`
  with commands pointing at `$HOME/.claude/hooks/spiral/…`. The hooks still only act in projects that have `spiral.config.json`.

Add `.spiral/state.json` to the project's `.gitignore`. It's per-machine run state.

## Stack presets (what `/spiral-init` fills in)

| Stack | typecheck / lint / test | UI capture |
|-------|-------------------------|------------|
| Next.js / React (Vite) | `tsc --noEmit`, `eslint`, `vitest run` or `jest` | `playwright` against `devUrl` |
| Node/Express API | `tsc --noEmit`, `eslint`, `vitest`/`jest` + `supertest` | `ui.enabled: false` |
| React Native / Expo | `tsc --noEmit`, `eslint`, `jest` (+ RNTL) | `command`: `xcrun simctl io booted screenshot {outDir}/{name}.png` or `adb exec-out screencap -p > {outDir}/{name}.png` |
| iOS (Swift) | `swift build` / `xcodebuild build`, `swiftlint`, `swift test` | `command`: `xcrun simctl io booted screenshot …` |
| Android (Kotlin) | `./gradlew compileDebugKotlin`, `./gradlew ktlintCheck`, `./gradlew testDebugUnitTest` | `command`: `adb exec-out screencap -p …` |
| Flutter | `flutter analyze`, `dart format --set-exit-if-changed .`, `flutter test` | `command` (golden files or simulator) |
| Python (Django/FastAPI) | `mypy .`, `ruff check .`, `pytest -q` | `playwright` if there is a web UI |
| Laravel / PHP | `phpstan analyse`, `pint --test`, `php artisan test` | `playwright` |

Spiral's own insight: behaviour tests must be **fast and CLI-run** (no simulator) so the loop is cheap. Prefer
headless integration tests over e2e-in-a-device for gate 1, and reserve the device for gate-2 screenshots.

## Playwright capture (web default)

The orchestrator writes a throwaway script into the checkpoint's `shots/` dir (never into the project's source), e.g.:

```js
// shots/capture.mjs — run with: node .spiral/runs/<slug>/cp-NN/shots/capture.mjs
import { chromium } from 'playwright';
const [url, out, w, h] = process.argv.slice(2);
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: +w, height: +h } });
await page.goto(url, { waitUntil: 'networkidle' });
await page.screenshot({ path: out, fullPage: true });
await browser.close();
```

Use deterministic data (fixtures/mocks/seeded DB) so reference and candidate show the same content.
