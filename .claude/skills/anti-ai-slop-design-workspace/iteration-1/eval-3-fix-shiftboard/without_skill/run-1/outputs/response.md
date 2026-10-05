I've redesigned the ShiftBoard dashboard. It's still one HTML file, with no external fonts, libraries or images.

**What the old version did wrong**
The purple gradient, glass cards, glowing buttons, emoji icons and "Welcome back, John Doe! 👋" are what make it look AI-generated. But the bigger problem was that it didn't answer either question a ward manager has at 07:30: where are the gaps, and who's on. "Total Staff 1,234" with a green +12.5%, "Efficiency 98%" and a chart with no data are numbers nobody acts on.

**How the new version is built around the shift**
- **The header is the shift itself.** It shows the ward, the date and "Day shift 07:30–20:00", with a toggle to switch to tonight's night shift. Below it is one summary line: unfilled shifts, RNs against plan with the patient ratio, HCAs against plan, and beds. Red is only used when something is short.
- **"Gaps to fill" comes first.** Each gap says what's missing (role, bay, hours), why (sickness at 05:40, or open since Friday) and where things stand (bank request viewed 4 times and accepted 0 times, interim cover by L. Byrne). Each one has the next action on it: escalate to agency, call the staff list, or approve a partial bank offer.
- **"On shift now" is a roster table**, grouped into RNs, HCAs and supernumerary. It shows the nurse in charge, band, bay allocation, hours and the clinical notes that matter at handover (IV competent, preceptee pairing, enhanced obs). Unfilled slots appear as red rows in their place on the roster, so the gap shows up where the person should be.
- **The right column covers what's coming:** tonight's planned vs booked staff, unfilled shifts for each of the next 7 days, and a short "since last handover" log (sickness calls, swaps and leave requests waiting for approval).

**Visual approach**
- The look is quiet and clinical: off-white paper, dark ink, thin rules and a system font, with tabular numbers and monospace times so columns line up when someone scans them. The only colours carry meaning: red for unfilled and amber for partly sorted.
- It has a dark mode that follows the device setting, which helps on night shifts and on dim nurses' station screens. It also has a print stylesheet so it can be printed for the handover board.
- It works at phone width: the columns stack and the hours column hides.

**Before you use it**
- All names, numbers and bleeps are placeholder data. Swap in real data before showing it to anyone.
- The buttons and the Day/Night toggle are visual only. The toggle changes its own state but doesn't swap the data yet.
- I assumed UK NHS conventions (bands, bank and agency, NIC, HCA). Tell me if your trust uses different terms or shift times.
