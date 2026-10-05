I've built your landing page as a single `index.html`. It's plain HTML and CSS with no JavaScript and no build step. The only outside resource is Google Fonts (Fraunces for headings, IBM Plex Sans and Mono for text).

**How it looks**
It uses warm paper and ink colours, a deep green and a brick accent, so it reads like a careful accountant rather than a fintech app. The main visual sits in the hero. It's a "payment trail" card that follows one $1,200 Upwork payment through Payoneer and into a Pakistani bank, then stops at the missing proceeds realisation certificate (PRC) and the return that hasn't been filed yet. That card explains what you do better than a stock photo could.

**Sections, in order**
1. **Header** with a "Book a call" button.
2. **Hero:** "You earn in dollars. File like it.", the payment trail card, and a note that calls are in Urdu or English.
3. **Platforms strip:** Upwork, Fiverr, Payoneer, Wise, Toptal and direct bank wires.
4. **Common questions:** the four worries freelancers actually bring (never filed, the bank asking for an NTN, tax on Payoneer money, income filed as "salary").
5. **Services:** NTN and ATL status, PSEB registration, annual return and wealth statement, remittance paperwork, FBR notices and back years.
6. **How it works:** a four-step timeline from the free call to the filed return, plus a "what to have ready" document checklist.
7. **Fees:** three fixed-fee plans in PKR.
8. **FAQ:** expandable answers using native `<details>` elements.
9. **Contact:** a WhatsApp button with a pre-filled message, email, office address and hours.
10. **Footer:** a disclaimer.

It works on phones and tablets (breakpoints at 900px and 560px). The navigation is hidden on mobile and the call-to-action button stays visible.

**Placeholders to replace before you go live**
- **Business name:** "Remit & Return" is a placeholder.
- **Contact details:** the WhatsApp number (`+92 300 0000000` and the `wa.me/923000000000` link), `hello@example.com`, and "Office address, Gulberg III".
- **Fees:** PKR 6,000 for registration, 15,000 a year for annual filing, and from 10,000 per back year. I made these numbers up, so set your own.
- **Example card amounts:** they are illustrative, and the card is labelled "Example".

**Please check the tax wording**
I kept the tax statements general on purpose and didn't quote rates, because the rates for IT export income, the PSEB rules and Punjab Revenue Authority sales tax change with each Finance Act. Before publishing, please confirm:
- the 30 September deadline wording
- the claim that most individual exporters don't need to register with the Punjab Revenue Authority
- the claim that PSEB registration affects the export rate

I didn't add testimonials, client counts or "trusted by" logos, because you're just launching and invented ones would be misleading. Add real ones once you have clients who agree to be quoted. A short quote from a known Lahore freelancer would sit well between the services and how-it-works sections.
