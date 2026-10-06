// Shared helpers for the Spiral hooks and CLI. No dependencies: Node 18+ only.
import { readFileSync, existsSync, writeFileSync, mkdirSync, appendFileSync } from 'node:fs';
import { join, resolve, relative, dirname, isAbsolute } from 'node:path';
import { createHash } from 'node:crypto';

export const PHASES = ['idle', 'plan', 'tests', 'implement', 'review', 'approval'];

export function readInput() {
  try {
    return JSON.parse(readFileSync(0, 'utf8') || '{}');
  } catch {
    return {};
  }
}

export function projectRoot(input = {}) {
  return resolve(process.env.CLAUDE_PROJECT_DIR || input.cwd || process.cwd());
}

// spiral.config.json is plain JSON, but tolerate // and /* */ comments outside strings.
function stripComments(text) {
  let out = '';
  let inStr = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    const n = text[i + 1];
    if (inStr) {
      out += c;
      if (c === '\\') out += text[++i] ?? '';
      else if (c === '"') inStr = false;
    } else if (c === '"') {
      inStr = true;
      out += c;
    } else if (c === '/' && n === '/') {
      while (i < text.length && text[i] !== '\n') i++;
      out += '\n';
    } else if (c === '/' && n === '*') {
      i += 2;
      while (i < text.length && !(text[i] === '*' && text[i + 1] === '/')) i++;
      i++;
    } else out += c;
  }
  return out.replace(/,(\s*[}\]])/g, '$1');
}

export function loadConfig(root) {
  const p = join(root, 'spiral.config.json');
  if (!existsSync(p)) return null;
  try {
    return JSON.parse(stripComments(readFileSync(p, 'utf8')));
  } catch (e) {
    return { __error: `spiral.config.json is not valid JSON: ${e.message}` };
  }
}

const statePath = (root) => join(root, '.spiral', 'state.json');

export function loadState(root) {
  try {
    return JSON.parse(readFileSync(statePath(root), 'utf8'));
  } catch {
    return { phase: 'idle', lockedTests: {} };
  }
}

export function saveState(root, state) {
  mkdirSync(join(root, '.spiral'), { recursive: true });
  state.updatedAt = new Date().toISOString();
  writeFileSync(statePath(root), JSON.stringify(state, null, 2) + '\n');
}

export function logEvent(root, state, line) {
  const dir = state.target && state.cp
    ? join(root, '.spiral', 'runs', state.target, `cp-${state.cp}`)
    : join(root, '.spiral');
  mkdirSync(dir, { recursive: true });
  appendFileSync(join(dir, 'phase.log'), `${new Date().toISOString()} ${line}\n`);
}

export const isActive = (state) => state.phase && state.phase !== 'idle';

// Project-relative, forward-slash path; lower-cased on Windows so comparisons are case-insensitive.
export function rel(root, p) {
  const abs = isAbsolute(p) ? p : resolve(root, p);
  let r = relative(root, abs).split('\\').join('/');
  if (process.platform === 'win32') r = r.toLowerCase();
  return r;
}

export function sha256File(root, relPath) {
  const p = join(root, relPath);
  if (!existsSync(p)) return null;
  return createHash('sha256').update(readFileSync(p)).digest('hex');
}

// Minimal glob: ** = any depth, * = within a segment. Patterns without "/" match the basename anywhere.
export function globToRegex(glob) {
  let g = glob.split('\\').join('/');
  if (process.platform === 'win32') g = g.toLowerCase();
  const body = g
    .replace(/[.+^${}()|[\]]/g, '\\$&')
    .replace(/\*\*/g, '\u0000')
    .replace(/\*/g, '[^/]*')
    .replace(/\?/g, '[^/]')
    .replace(/\u0000/g, '.*');
  return g.includes('/') ? new RegExp(`^${body}$`) : new RegExp(`(^|/)${body}$`);
}

// Config and tooling files the implementer may not touch during a run (loosening them is how agents "get green").
export const DEFAULT_PROTECTED = [
  'spiral.config.json',
  '.spiral/state.json',
  '.eslintrc*', 'eslint.config.*', '.prettierrc*', 'biome.json*', '.stylelintrc*',
  'tsconfig*.json', 'jsconfig*.json',
  'jest.config.*', 'vitest.config.*', 'vitest.workspace.*', 'playwright.config.*', 'cypress.config.*',
  'ruff.toml', '.ruff.toml', 'mypy.ini', 'pytest.ini', 'tox.ini', '.flake8',
  'phpstan.neon*', 'phpunit.xml*', 'pint.json',
  '.swiftlint.yml', 'detekt.yml', '.editorconfig', 'analysis_options.yaml', '.golangci.*',
  '.github/workflows/**', '.gitlab-ci.yml', '.husky/**',
];

export function protectedMatchers(config) {
  const extra = config?.guard?.protected ?? [];
  return [...DEFAULT_PROTECTED, ...extra].map(globToRegex);
}

export function testsDir(config) {
  const d = config?.tests?.dir;
  return d && d !== 'colocated' ? d.replace(/\\/g, '/').replace(/\/$/, '') : null;
}

// Lint/type/test suppressions. A line is allowed if it carries "spiral-allow: <reason>".
export const SUPPRESSIONS = [
  [/eslint-disable/, 'eslint-disable'],
  [/@ts-(ignore|nocheck|expect-error)/, '@ts-ignore/@ts-nocheck/@ts-expect-error'],
  [/biome-ignore/, 'biome-ignore'],
  [/#\s*type:\s*ignore/, '# type: ignore'],
  [/#\s*noqa/, '# noqa'],
  [/(pylint|pyright):\s*(disable|ignore)/, 'pylint/pyright disable'],
  [/@Suppress(Warnings)?\s*\(/, '@Suppress'],
  [/swiftlint:disable/, 'swiftlint:disable'],
  [/\/\/\s*nolint/, '//nolint'],
  [/@phpstan-ignore/, '@phpstan-ignore'],
  [/\b(it|test|describe|context)\.(skip|only|todo)\s*\(/, '.skip/.only/.todo test'],
  [/\bx(it|describe|test)\s*\(/, 'xit/xdescribe'],
  [/@pytest\.mark\.(skip|xfail)/, 'pytest skip/xfail'],
  [/@(Disabled|Ignore)\b/, '@Disabled/@Ignore'],
];

export function findSuppressions(addedLines) {
  const hits = [];
  for (const line of addedLines) {
    if (/spiral-allow:\s*\S{3,}/.test(line)) continue;
    for (const [re, label] of SUPPRESSIONS) {
      if (re.test(line)) {
        hits.push(`${label}: ${line.trim().slice(0, 120)}`);
        break;
      }
    }
  }
  return hits;
}

export function deny(reason) {
  process.stdout.write(JSON.stringify({
    hookSpecificOutput: {
      hookEventName: 'PreToolUse',
      permissionDecision: 'deny',
      permissionDecisionReason: `[spiral guard] ${reason}`,
    },
  }));
  process.exit(0);
}

export { existsSync, dirname, join };
