// PostToolUse (Edit|Write|MultiEdit): during an active Spiral run, lints the edited file with
// commands.lintFile so mistakes surface immediately instead of at gate 1.
import { execSync } from 'node:child_process';
import { readInput, projectRoot, loadConfig, loadState, isActive, rel } from './lib.mjs';

const input = readInput();
const root = projectRoot(input);
const config = loadConfig(root);
const tpl = config?.commands?.lintFile;
if (!tpl) process.exit(0);
const state = loadState(root);
if (!isActive(state)) process.exit(0);

const file = input.tool_input?.file_path;
if (!file) process.exit(0);
const r = rel(root, file);
if (r.startsWith('..') || r.startsWith('.spiral/') || r.endsWith('.md')) process.exit(0);
const exts = config?.guard?.lintExtensions ?? ['.js', '.jsx', '.ts', '.tsx', '.mjs', '.cjs', '.vue', '.svelte', '.py', '.php', '.kt', '.swift', '.dart', '.go', '.rb'];
if (!exts.some((e) => r.endsWith(e))) process.exit(0);

try {
  execSync(tpl.replace('{file}', JSON.stringify(file)), { cwd: root, stdio: 'pipe', timeout: 60_000 });
} catch (e) {
  if (e.code === 'ETIMEDOUT' || e.signal) process.exit(0); // slow lint is gate 1's job, not this hook's
  const out = `${e.stdout ?? ''}${e.stderr ?? ''}`.trim().slice(-3000);
  process.stdout.write(JSON.stringify({
    decision: 'block',
    reason: `[spiral quick-check] lint failed for ${r}. Fix before moving on:\n${out}`,
  }));
}
process.exit(0);
