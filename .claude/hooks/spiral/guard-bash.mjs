// PreToolUse (Bash|PowerShell): during an active Spiral run, blocks history-rewriting / publishing git
// commands, hook bypasses, and shell writes to locked tests, protected config, or Spiral state.
import {
  readInput, projectRoot, loadConfig, loadState, isActive, rel, protectedMatchers, deny,
} from './lib.mjs';

const input = readInput();
const root = projectRoot(input);
const config = loadConfig(root);
if (!config) process.exit(0);
const state = loadState(root);
const cmd = String(input.tool_input?.command ?? '');
if (!cmd) process.exit(0);
const usesCli = /spiral\.mjs/.test(cmd);

if (/\.spiral[\\/]state\.json/.test(cmd) && !usesCli && /(>|\bsed\b|\brm\b|\bmv\b|\bcp\b|Set-Content|Out-File|Remove-Item)/.test(cmd)) {
  deny('.spiral/state.json is managed by spiral.mjs only.');
}

if (!isActive(state)) process.exit(0);

const BLOCKED = [
  [/\bgit\s+push\b/, 'git push. Spiral never publishes; the engineer pushes.'],
  [/--no-verify\b|\bgit\s+commit\b[^|;&]*\s-n\b/, 'skipping git hooks (--no-verify / -n)'],
  [/\bgit\s+reset\s+--hard\b/, 'git reset --hard'],
  [/\bgit\s+clean\s+-[a-z]*f/, 'git clean -f'],
  [/\bgit\s+rebase\b/, 'git rebase'],
  [/\bgit\s+commit\b[^|;&]*--amend\b/, 'git commit --amend (rewrites an approved checkpoint)'],
  [/\bgit\s+(checkout|switch)\s+(main|master|develop)\b/, 'leaving the spiral branch mid-run'],
  [/\bgit\s+merge\b/, 'git merge'],
  [/\bgh\s+pr\s+(create|merge)\b/, 'creating/merging PRs. Only the engineer does that.'],
];
for (const [re, why] of BLOCKED) if (re.test(cmd)) deny(`blocked during a Spiral run: ${why}.`);

// Shell writes to locked tests / protected config. Ignore harmless redirects like 2>&1 and >/dev/null.
const cleaned = cmd.replace(/\d*>&\d+/g, '').replace(/\d*>\s*(\/dev\/null|\$null|nul)\b/gi, '');
const WRITES = /(>|\bsed\s+-i|\bperl\s+-\w*i|\brm\b|\bmv\b|\bcp\b|\btee\b|\btruncate\b|\bgit\s+(checkout|restore|rm|mv)\b|Set-Content|Add-Content|Out-File|Remove-Item|Move-Item|Copy-Item|Clear-Content|\bdel\b|\bren\b|writeFile)/i;
if (!usesCli && WRITES.test(cleaned)) {
  const tokens = cleaned.match(/"[^"]*"|'[^']*'|[^\s;|&<>()]+/g) ?? [];
  const locked = state.phase === 'tests' ? [] : Object.keys(state.lockedTests ?? {});
  const prot = protectedMatchers(config);
  for (const t of tokens) {
    const p = t.replace(/^['"]|['"]$/g, '');
    if (!p || p.startsWith('-')) continue;
    const r = rel(root, p);
    if (locked.includes(r)) deny(`shell command modifies locked Spiral test ${r}. Tests are owned by spiral-test-writer.`);
    if (prot.some((re) => re.test(r))) deny(`shell command modifies protected config ${r} during a Spiral run.`);
  }
}
process.exit(0);
