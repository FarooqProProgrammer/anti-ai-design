# Design Sources: check MCP servers first

Connected design tools give you the *real* design: exact variables, real screenshots, real shipped apps. That beats guessing from memory or from a web search. So at the start of every task, detect what the user gave you and check which design MCP servers are connected before doing anything else.

## Contents
1. Step 0: detect and check (do this first)
2. Figma
3. Mobbin
4. Browser
5. When a server is missing or needs authentication

---

## 1. Step 0: detect and check (do this first)

**A. Detect triggers in the user's message and in the project:**

| Trigger | Source to check |
|---|---|
| A `figma.com/...` URL (`/design/`, `/file/`, `/proto/`, `/board/`, `/slides/`, `/make/`) | **Figma MCP** |
| "Figma", "my design file", "the mockups", "design system in Figma" | **Figma MCP** (ask for the link if none was given) |
| "Mobbin", "real app examples", "how do other apps do X", or any reference hunt, especially for app UI, flows or dashboards | **Mobbin MCP** (pre-check proactively) |
| A live website URL to match or audit | Browser tool (screenshots), else `ref_board.py fetch` |

**B. Check whether the server is available, without guessing:**

1. Look at the tools you already have, and at the deferred-tool list in the system reminders, for names containing `figma` or `mobbin` (e.g. `mcp__claude_ai_Figma__*`, `mcp__figma__*`, `mcp__claude_ai_Mobbin__*`). Exact prefixes differ between installs, so match on the keyword.
2. If the tools are deferred, load them with **one** ToolSearch call. For example: `select:<figma get_design_context>,<get_screenshot>,<get_variable_defs>,<get_metadata>` or `select:<mobbin search_screens>,<search_sections>,<search_flows>`. A keyword query such as `figma` or `mobbin` also works.
3. Check whether the server is listed as **"requires authentication"** or **"failed to connect"**. If so, it's unavailable: follow §5.

**C. Say what you found in one line, then route:**
- "Figma is connected — reading your file first."
- "Mobbin is connected — I'll pull real app screens for references."
- "Figma isn't connected — here's how to connect it, or send screenshots."

Then follow the mode as usual (Build, Fix, Reference hunt, Brand book), with the connected source ranked first.

## 2. Figma

**A Figma file is the user's own design or design system.** It sits at the top of the signal ladder: it overrides your taste, the references and the defaults. Your job is to implement it faithfully, and to apply the slop catalog only to gaps the file doesn't cover. Point out problems (e.g. low contrast); don't silently "improve" them.

**Parsing the URL:**
- `figma.com/design/<fileKey>/<name>?node-id=1-2` gives fileKey `<fileKey>` and nodeId `1:2`.
- For a branch URL (`/design/<fileKey>/branch/<branchKey>/…`), use the `branchKey` as the fileKey.
- `/make/<makeFileKey>/…` is a Figma Make file: use it only with `get_design_context`, with nodeId `0:1`.
- No `node-id` in the link: call `get_metadata` with only the fileKey to list the pages. Then pick the relevant frame, or ask the user for a link to the specific frame. Never guess a nodeId.

**Order of calls (read-only, for implementing or auditing):**
1. `get_metadata`: the structure (pages, frames, IDs, sizes).
2. `get_screenshot`: *look* at the design before anything else.
3. `get_variable_defs`: the file's variables (colors, type, spacing, radius). These become your tokens. When making a brand book, map them into `brand.json` instead of inventing values.
4. `get_design_context`: reference code, assets and a screenshot for a node. **First load the Figma design-to-code guidance**: the `/figma-design-to-code` skill if listed, otherwise the `skill://figma/figma-design-to-code/SKILL.md` MCP resource. The tool requires this. Adapt the returned code to the project's stack and existing components; don't paste it in raw.
5. Optional:
   - `search_design_system` or `get_libraries` to find the file's components.
   - `get_code_connect_map` to see which code components the Figma components map to.

**Writing to Figma** (e.g. pushing a brand book or design onto the canvas): load the `/figma-use` skill first, which Figma's own instructions make mandatory before `use_figma`, along with the relevant Figma skills such as `/figma-generate-design` and `/figma-generate-library`.

**How it fits each mode:**
- **Build:** tokens come from `get_variable_defs`, layout from the screenshot and design context, and the scanner runs on your output only.
- **Audit:** screenshot the frames and audit them against the slop catalog. Cite them by frame name or node ID.
- **Reference hunt:** if the user has a Figma file, it's the anchor. Hunt only for the gaps it doesn't cover.
- **Brand book:** variables go into `colors`, `typography` and `layout`. Logos and icons can be exported via `get_design_context` asset URLs or `download_assets`.

## 3. Mobbin

Mobbin is a library of real, shipped app and web UI with screenshots. It's the best reference source for app screens, flows and website sections, so check it proactively in every reference hunt, not only when the user names it.

**Which tool to use:**

| Need | Tool | Key params |
|---|---|---|
| One screen ("checkout with promo code field") | `search_screens` | `query`, `platform` (`web`/`ios`) |
| A website section (hero, pricing, footer) | `search_sections` | `query` (web only) |
| A multi-step journey (onboarding, checkout) | `search_flows` | `query`, `platform`, small `limit` |

**How to call it:**
- **One screen, section or flow per query,** described concretely. No style adjectives ("modern, clean"), no negations, no keyword lists. Add an app name to filter by app ("Stripe pricing page").
- **Keep `task_intent` and `output_destination` the same across all calls in one task.** `task_intent` is one English sentence describing the task. `output_destination` is usually `code` in a repository.
- **Keep `limit` modest** (8–15 screens, 3–5 flows) to save context. Use `mode: "deep"` (the default) for nuanced queries.

**Using the results:**
- **Look at the returned images.** Judge from pixels, not from the metadata. These are your "seen" references for scoring.
- **Cite every screen you mention** as a markdown link to its `mobbin_url`.
- **If a result includes `ai_usage_notice`,** show its text to the user word for word, as its own block after the results.
- **On the reference board,** put the `mobbin_url` in `url` and set `source: "mobbin"`. For the image, download `image_url` (the high-res version) into `<scratchpad>/refs/` with `ref_board.py fetch <image_url> <dir>`, because these URLs expire after 30 days. Don't rely on the inline previews.
- **Combine with web search** for brand/visual direction (land-book, godly, fontsinuse). Mobbin is strongest for UI patterns and flows, and the web galleries for overall look.

## 4. Browser

If a browser automation tool is connected, use it to screenshot live sites (references, the user's current site, or your own built page for self-review). Follow that tool's own skill or instructions, such as loading all its tools in one ToolSearch call and opening a new tab. If none is available, fall back to `ref_board.py fetch` (og:image) and opening local files.

## 5. When a server is missing or needs authentication

- **Don't pretend.** Never claim to have read a Figma file or searched Mobbin when the tool isn't available.
- **Don't WebFetch a `figma.com` link** as a substitute. It needs a login, and returns nothing useful.
- **Tell the user plainly and briefly**, then offer a fallback:
  - **Needs authentication:** "Figma/Mobbin is configured but needs authorization — connect it in your claude.ai connector settings (or `/mcp` in an interactive Claude Code session), then ask again." Don't ask the user for tokens or codes.
  - **Failed to connect:** say it failed, so they can fix or retry it.
  - **Not installed:** mention that the server exists and that connecting it improves results.
- **Fallbacks:**
  - Figma: ask for exported PNG screenshots of the frames and a list or export of the colors, fonts and spacing (or the variables as JSON).
  - Mobbin: continue the reference hunt with web search and `ref_board.py fetch`, and say that the results are web-only.
- **If the request depends entirely on the server** (e.g. "implement this Figma frame"), stop after explaining and wait. Don't build from a guess.
