// PreToolUse (Edit|Write|MultiEdit|NotebookEdit): blocks, during an active Spiral run,
//  - edits to locked tests outside the "tests" phase,
//  - edits to lint/type/test/CI config and Spiral state,
//  - newly added lint/type/test suppressions without "spiral-allow: <reason>".
import {
  readInput, projectRoot, loadConfig, loadState, isActive, rel,
  protectedMatchers, testsDir, findSuppressions, deny,
} from './lib.mjs';

const input = readInput();
const root = projectRoot(input);
const config = loadConfig(root);
if (!config) process.exit(0); // not a Spiral project
const state = loadState(root);
const ti = input.tool_input ?? {};
const file = ti.file_path ?? ti.notebook_path;
if (!file) process.exit(0);
const r = rel(root, file);

// State is only ever changed through spiral.mjs, in any phase.
if (r === '.spiral/state.json') deny('.spiral/state.json is managed by spiral.mjs. Use `node <spiral>/spiral.mjs phase …` instead.');

if (!isActive(state)) process.exit(0);
if (r.startsWith('..')) process.exit(0); // outside the project

if (state.phase !== 'tests') {
  const locked = Object.keys(state.lockedTests ?? {});
  const td = testsDir(config);
  if (locked.includes(r) || (state.phase === 'implement' && td && (r === td || r.startsWith(td.toLowerCase() + '/')))) {
    deny(`${r} is a Spiral test and is locked during "${state.phase}". The implementer may not change tests. ` +
      'If the test is wrong, explain why in gate-1.md and re-launch spiral-test-writer (phase "tests").');
  }
}

// In "plan" the Spec Kit skills legitimately write .specify/** and specs/**; the guard only protects them once building starts.
const specArtifact = r.startsWith('.specify/') || r.startsWith('specs/');
if (!(state.phase === 'plan' && specArtifact) && protectedMatchers(config).some((re) => re.test(r))) {
  deny(`${r} is protected tooling/config during a Spiral run. Loosening lint, type, test or CI config is not a fix. ` +
    'Escalate to the engineer if it truly needs to change.');
}

// Only lines that are new count, so existing suppressions in a file don't block unrelated edits.
let added = [];
const before = new Set();
if (input.tool_name === 'Write') {
  added = String(ti.content ?? '').split('\n');
} else if (input.tool_name === 'MultiEdit') {
  for (const e of ti.edits ?? []) {
    String(e.old_string ?? '').split('\n').forEach((l) => before.add(l));
    added.push(...String(e.new_string ?? '').split('\n'));
  }
} else if (input.tool_name === 'NotebookEdit') {
  added = String(ti.new_source ?? '').split('\n');
} else {
  String(ti.old_string ?? '').split('\n').forEach((l) => before.add(l));
  added = String(ti.new_string ?? '').split('\n');
}
added = added.filter((l) => !before.has(l));

const hits = findSuppressions(added);
if (hits.length) {
  deny(`new suppression(s) in ${r}:\n- ${hits.join('\n- ')}\n` +
    'Fix the underlying issue. If a suppression is genuinely right, add "spiral-allow: <reason>" on the same line. ' +
    'Reviewers and the engineer will see it.');
}
process.exit(0);
