/** LEGACY - Tailwind CSS v3 projects only. On v4 (current) use tailwind.theme.css instead.
 *  Requires tokens.css to be loaded. */
module.exports = {
  "theme": {
    "extend": {
      "colors": {
        "paper": "var(--color-paper)",
        "ledger-ink": "var(--color-ledger-ink)",
        "ledger-green": "var(--color-ledger-green)",
        "folio": "var(--color-folio)",
        "rule": "var(--color-rule)",
        "stone": "var(--color-stone)",
        "debit-red": "var(--color-debit-red)",
        "ochre": "var(--color-ochre)",
        "credit-green": "var(--color-credit-green)",
        "bg": "var(--color-bg)",
        "text": "var(--color-text)",
        "accent": "var(--color-accent)",
        "on-accent": "var(--color-on-accent)",
        "surface": "var(--color-surface)",
        "border": "var(--color-border)",
        "muted": "var(--color-muted)"
      },
      "fontFamily": {
        "display": [
          "var(--font-display)"
        ],
        "body": [
          "var(--font-body)"
        ],
        "mono": [
          "var(--font-mono)"
        ]
      },
      "borderRadius": {
        "sm": "var(--radius-sm)",
        "md": "var(--radius-md)",
        "lg": "var(--radius-lg)"
      },
      "boxShadow": {
        "flat": "var(--shadow-flat)",
        "raised": "var(--shadow-raised)"
      },
      "fontSize": {
        "display": "var(--text-display)",
        "h1": "var(--text-h1)",
        "h2": "var(--text-h2)",
        "h3": "var(--text-h3)",
        "body": "var(--text-body)",
        "small": "var(--text-small)",
        "figure": "var(--text-figure)"
      }
    }
  }
};
