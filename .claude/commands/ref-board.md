---
description: Search the web for design references, analyze and rank them module-by-module against your brief, build a visual board, and let you pick the best reference per module.
argument-hint: <what you're designing, for whom — e.g. "landing page for a Lahore tax firm for freelancers">
allowed-tools: Read, Write, Bash, WebSearch, WebFetch, AskUserQuestion, ToolSearch, mcp__claude_ai_Mobbin__search_screens, mcp__claude_ai_Mobbin__search_sections, mcp__claude_ai_Mobbin__search_flows, mcp__claude_ai_Figma__get_metadata, mcp__claude_ai_Figma__get_screenshot, mcp__claude_ai_Figma__get_variable_defs, mcp__claude_ai_Figma__get_design_context
---

Run the **Reference hunt** from the `anti-ai-slop-design` skill for this brief:

> $ARGUMENTS

Follow `.claude/skills/anti-ai-slop-design/references/web-references.md` end to end. Read it first. In short:

0. **Check sources first** (`references/design-sources.md`).
   - Look for Figma and Mobbin MCP tools, and load deferred ones with one ToolSearch call.
   - Say in one line what's connected.
   - If the user included a Figma link and Figma is connected, read that file first; it anchors the hunt.
   - If Mobbin is connected, it's the first search source.
   - If either needs authentication or failed to connect, say so and continue with the web-only fallback.
1. **Brief.** Turn the request above into the brief block: subject, audience, three traits, content shape, must-haves, constraints, avoid.
   - If `$ARGUMENTS` is empty or too thin to rank against, ask up to 3 short questions first: what it is, who it's for, any must-haves or brand constraints.
   - If the user already gave a brand guide or references, say so, and use the hunt only to fill gaps.
2. **Modules.** Choose 4–7 modules to pick for. Design dimensions: Typography, Color, Layout, Imagery. Page modules from the brief: Hero, Pricing, Trust & proof, Navigation… (for apps: Shell, Tables, Charts…). Give each a one-line "need".
3. **Search.** Use UI-library MCP tools if connected (e.g. Mobbin), then WebSearch on galleries of real, shipped work and on admired sites in the domain. Gather 8–15 candidates across at least 3 distinct directions.
4. **See them.** Save images under the session scratchpad in `refs/`:
   ```bash
   python .claude/skills/anti-ai-slop-design/scripts/ref_board.py fetch <url> <scratchpad>/refs
   ```
   Then view each saved image with Read, or take screenshots with a browser tool if available. Mark anything you couldn't see as `"seen": false`.
5. **Analyze and score.**
   - Overall: score each reference on the six criteria.
   - Per module: a 1–5 score against that module's need, plus a one-line note.
   - Rerank for diversity and keep the best 4–6.
6. **Board.** Copy `.claude/skills/anti-ai-slop-design/assets/example-refs.json` to `<scratchpad>/refs/refs.json`, fill it in, then render and open it:
   ```bash
   python .claude/skills/anti-ai-slop-design/scripts/ref_board.py board <scratchpad>/refs/refs.json <scratchpad>/refs/board.html
   ```
   On Windows, open it with `Start-Process <path>`. Elsewhere, use `open` (macOS) or `xdg-open` (Linux).
7. **Ask.**
   - In chat: the overall ranking (one line each), then each module's recommendation and runner-up.
   - Ask the user to pick per module with AskUserQuestion: one question per module, the top 3 references as options with the recommended one first, at most 4 questions per call. Or have them press **Copy choices** on the board and paste the result.
   - Wait for their answers.
8. **Digest.** Write the per-module reference digest (borrow / adapt / don't copy, plus any conflicts between picks). Then offer the next step: build the page, or make a brand book with `/brand-book`.

Don't build anything before the user has picked.
