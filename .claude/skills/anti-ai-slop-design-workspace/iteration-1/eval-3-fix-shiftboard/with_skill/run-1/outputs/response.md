I've redesigned the ShiftBoard dashboard. It's still one HTML file, at `outputs/dashboard.html`. The only thing it loads from outside is IBM Plex from Google Fonts, and it falls back to system fonts if that fails.

**What was wrong with the old one.** The slop scanner found 11 separate signs of a generic AI design, which it rates as high. The page had:
- an indigo-to-purple gradient background
- a gradient-text logo
- glassmorphism cards with glowing edges
- emoji used as icons
- "Supercharge your ward scheduling with AI-powered insights"
- "Welcome back, John Doe!" and Jane Smith as placeholder names
- four KPI cards with green "+12.5%" pills
- an empty gradient box standing in for a chart
- `hover: scale(1.05)` on every card

The structural problem mattered more than the colours. Nothing on the page answered what a ward manager wants to know at 07:15: *where are the gaps, and who's on?* "Total Staff 1,234" and "Efficiency 98%" don't help anyone run a shift.

**The approach.** I based it on the ward whiteboard, made precise. The design rules I followed:
- **Paper background.** A warm off-white with near-black text, since it gets read under ward lighting at the nurses' station.
- **One colour with one job.** Marker red always and only means "short-staffed". Amber marks shifts that are covered but fragile (bank staff, no spare).
- **Fonts.** IBM Plex Sans Condensed for headings, Plex Sans for body text, and Plex Mono for times and counts so the numbers line up.

**What changed and why**
1. **The worst gap leads the page.** A large red **−2** sits next to "Tonight's night shift is two registered nurses short", with the reason and one clear action: "Request 2 bank RNs for tonight".
2. **The four KPI cards became one strip of figures** a manager actually uses: unfilled shifts in the next 7 days (broken down by RN and HCA), staff on the ward now against the number needed, staff off sick, and bank/agency hours against budget.
3. **The fake chart became a week grid.** It shows Early, Late and Night for each day as rostered/required (e.g. `5/7`), with short shifts in red and fragile ones in amber. Today's column is dark and the current shift is outlined. On a phone the grid scrolls inside its own box.
4. **"Who's on" is a proper handover table.** It lists name, band, bays and break time, marks the nurse in charge and bank staff, and has a line for who arrives at 13:30. There's also a "Print handover sheet" link.
5. **"Recent Activity" became "Since last handover".** Each entry says what it does to cover, e.g. a sick call that leaves the Late today, tonight's Night and Wednesday's Early uncovered. The "View All 🚀" glow button is now a plain "Full change log →" link.
6. **The glass sidebar became a dark top bar** with text-only navigation. "Dashboard" is now "Today" and "Analytics" is now "Reports". The navigation stays the same otherwise.
7. **Removed:** emoji, gradients, blur, glows, hover-scale and `transition: all`. The only animation left is a 150ms colour change on hover, and it is turned off for users who set reduced motion.
8. **Accessibility basics:** real `<table>` markup with headers, visible focus outlines, text labels alongside every colour (for example "2 RN short", not just red), and a layout that works at 375px with no sideways page scroll.

**Checks.** The scanner now reports 0 tells. For a swap test I replaced "ShiftBoard" with an unrelated product, and the page made no sense, which is the goal. Bands, bays, NIC, bank cover and the Early/Late/Night pattern all belong to this ward.

**Things to check against your real system.** The data is sample data I made up to look plausible: Ward 7B, the staff names, the shift times (07:30–15:30, 13:30–21:30, 21:00–07:45) and the staffing numbers (6 RN + 3 HCA for days, 5 RN + 2 HCA for nights). Swap in your real shift patterns and safe-staffing numbers. The "Request bank RNs" button and the other links don't go anywhere yet (`href="#"`).
