# DESIGN.md — Diaw Trading Import-Export

Diaw Trading inherits the GeoTrading design system (see `GEOTRADING-DESIGN.md`) with these overrides for the import-export vertical.

## Brand Overrides

| Token | GeoTrading Default | Diaw Trading Override |
|-------|-------------------|----------------------|
| Logo text | GeoTrading | Diaw Trading |
| Tagline | "Trade Beyond Borders" | "Connecting Senegal to the World" |
| Primary market | UAE | Senegal / West Africa |
| Accent secondary | Emerald #10B981 | Teal #14B8A6 (warmer, West African palette) |

## Additional Color — Terracotta Accent

| Role | Token | Value | Usage |
|------|-------|-------|-------|
| Terracotta | --accent-terracotta | #C2724F | West African warmth accent, agriculture section headers |
| Terracotta faint | --accent-terracotta-faint | rgba(194,114,79,0.10) | Agro-business section backgrounds |

## Diaw-Specific Components

**HS Code Lookup Card**: bg `--bg-surface`, header "HS Classification" in overline style, code display JetBrains Mono 20px/700 in gold, description 14px Inter, duty-rate badge (emerald=low, amber=medium, crimson=high), origin/destination flags as inline 20px emoji.

**Shipping Status Timeline**: vertical, left-aligned. Active step = gold dot (12px) + gold connecting line. Completed = emerald dot + line. Pending = slate dot + dashed line. Labels 13px/500 Inter, timestamps 12px JetBrains Mono in text-tertiary.

**Trade Document (Invoice/BL)**: print-optimized A4. Header: Diaw Trading logo + RCCM SN DKR 2021 A 21531 + NINEA 008663248. Gold 2px horizontal rule under header. Banking footer: UBA + CBAO details in monospace. All amounts in XOF, JetBrains Mono.

## Typography Addition (French content)

- Use "Inter" — excellent support for French diacritics (é, è, ê, ë, ç)
- Maintain same size hierarchy as GeoTrading base
- Quotation marks: use «guillemets» for French text

All other tokens, components, layout, and rules inherit from `GEOTRADING-DESIGN.md`.
