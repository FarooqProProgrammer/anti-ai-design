#!/usr/bin/env node
// Spiral run-state CLI. The only sanctioned way to change .spiral/state.json.
//
//   spiral.mjs phase <idle|plan|tests|implement|review|approval> [--target <slug>] [--cp <NN>] [--reason "<why>"]
//   spiral.mjs lock-tests [files…]   record sha256 of the test files (default: changed/untracked files in tests.dir)
//   spiral.mjs verify-tests          exit 1 if any locked test changed since it was locked (run first in gate 1)
//   spiral.mjs status                print state + whether the hooks will be active
import { execSync } from 'node:child_process';
import {
  projectRoot, loadConfig, loadState, saveState, logEvent, PHASES, rel, sha256File, testsDir,
} from './lib.mjs';

const root = projectRoot();
const config = loadConfig(root);
if (!config) fail('No spiral.config.json in this project. Run /spiral-init first.');
if (config.__error) fail(config.__error);

const [cmd, ...rest] = process.argv.slice(2);
const flags = {};
const positional = [];
for (let i = 0; i < rest.length; i++) {
  if (rest[i].startsWith('--')) flags[rest[i].slice(2)] = rest[i + 1]?.startsWith('--') ? true : rest[++i] ?? true;
  else positional.push(rest[i]);
}
const state = loadState(root);
state.lockedTests ??= {};
state.testsEntries ??= {};

switch (cmd) {
  case 'phase': {
    const phase = positional[0];
    if (!PHASES.includes(phase)) fail(`phase must be one of: ${PHASES.join(', ')}`);
    if (flags.target) state.target = flags.target;
    if (flags.cp) state.cp = String(flags.cp).padStart(2, '0');
    if (phase === 'tests') {
      const key = `${state.target}/cp-${state.cp}`;
      const n = (state.testsEntries[key] ?? 0) + 1;
      // Re-entering "tests" in the same checkpoint unlocks the tests again, so it has to be justified and is logged.
      if (n > 1 && !flags.reason) fail('Re-entering "tests" for the same checkpoint needs --reason "<why the tests must change>".');
      state.testsEntries[key] = n;
    }
    const from = state.phase ?? 'idle';
    state.phase = phase;
    if (phase === 'idle' && flags['target-done']) state.cp = null;
    saveState(root, state);
    logEvent(root, state, `phase ${from} -> ${phase}${flags.reason ? ` reason="${flags.reason}"` : ''}`);
    console.log(`spiral: phase ${from} -> ${phase} (${state.target ?? '-'} cp-${state.cp ?? '-'})`);
    break;
  }

  case 'lock-tests': {
    if (state.phase !== 'tests') fail('lock-tests only runs in the "tests" phase (right after spiral-test-writer).');
    let files = positional.map((f) => rel(root, f));
    if (!files.length) {
      const dir = testsDir(config);
      if (!dir) fail('tests.dir is "colocated": pass the test files explicitly.');
      const out = execSync(`git status --porcelain --untracked-files=all -- "${dir}"`, { cwd: root, encoding: 'utf8' });
      files = out.split('\n').filter(Boolean)
        .filter((l) => !l.startsWith(' D') && !l.startsWith('D '))
        .map((l) => rel(root, l.slice(3).replace(/^"|"$/g, '').split(' -> ').pop()));
    }
    if (!files.length) fail('No test files to lock: did spiral-test-writer write anything?');
    for (const f of files) {
      const h = sha256File(root, f);
      if (!h) fail(`Not found: ${f}`);
      const prev = state.lockedTests[f];
      state.lockedTests[f] = h;
      logEvent(root, state, `${prev ? (prev === h ? 'lock (unchanged)' : 'RELOCK (changed)') : 'lock'} ${f}`);
    }
    saveState(root, state);
    console.log(`spiral: locked ${files.length} test file(s):\n  ${files.join('\n  ')}`);
    break;
  }

  case 'verify-tests': {
    const bad = [];
    for (const [f, h] of Object.entries(state.lockedTests)) {
      const now = sha256File(root, f);
      if (now !== h) bad.push(`${now ? 'modified' : 'deleted'}: ${f}`);
    }
    if (bad.length) {
      logEvent(root, state, `verify-tests FAIL ${bad.join(', ')}`);
      console.error(`spiral: locked tests changed outside the "tests" phase. Gate 1 fails:\n  ${bad.join('\n  ')}\n` +
        'Restore them (git checkout -- <file> as the engineer), or re-launch spiral-test-writer with a reason.');
      process.exit(1);
    }
    console.log(`spiral: ${Object.keys(state.lockedTests).length} locked test file(s) intact.`);
    break;
  }

  case 'status':
    console.log(JSON.stringify({ ...state, hooksActive: (state.phase ?? 'idle') !== 'idle' }, null, 2));
    break;

  default:
    fail('usage: spiral.mjs <phase|lock-tests|verify-tests|status> …');
}

function fail(msg) {
  console.error(`spiral: ${msg}`);
  process.exit(2);
}
