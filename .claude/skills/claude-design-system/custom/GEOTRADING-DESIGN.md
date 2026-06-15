# DESIGN.md — GeoTrading General Trading LLC / Diaw Trading

## 1. Visual Theme & Atmosphere

GeoTrading's visual identity fuses West African warmth with Dubai precision. The interface communicates intercontinental power. The aesthetic is dark-sovereign: deep navy canvases punctuated by gold accents used sparingly — like real gold, its value comes from scarcity.

Design philosophy: "Authority without arrogance." A Bloomberg terminal redesigned with West African / Gulf sensibility. Dense with information but never cluttered.

Mood keywords: Intercontinental. Sovereign. Precise. Warm-dark. Technical luxury.

Density: Medium-high. Whitespace is used structurally, not decoratively.

## 2. Color Palette & Roles

| Role | Token | Value | Usage |
|------|-------|-------|-------|
| Canvas | --bg-canvas | #0A1628 | Page background |
| Surface | --bg-surface | #0F1D32 | Cards, panels, elevated containers |
| Surface raised | --bg-raised | #162440 | Modals, dropdowns, overlays |
| Gold accent | --accent-gold | #D4AF37 | Primary CTA, active states, revenue. Used SPARINGLY |
| Gold muted | --accent-gold-muted | #B8962E | Secondary gold for borders |
| Gold faint | --accent-gold-faint | rgba(212,175,55,0.08) | Selected rows, active tab backgrounds |
| Emerald | --accent-emerald | #10B981 | Success, profit, positive delta |
| Emerald faint | --accent-emerald-faint | rgba(16,185,129,0.10) | Profit row backgrounds |
| Crimson | --color-danger | #EF4444 | Loss, error, negative delta |
| Crimson faint | --color-danger-faint | rgba(239,68,68,0.10) | Loss row backgrounds |
| Azure | --color-info | #3B82F6 | Informational, links, in-transit status |
| Amber | --color-warning | #F59E0B | Pending, awaiting approval |
| Text primary | --text-primary | #F1F5F9 | Headlines, body, primary content |
| Text secondary | --text-secondary | #94A3B8 | Labels, captions, metadata |
| Text tertiary | --text-tertiary | #64748B | Disabled text, placeholders |
| Border default | --border-default | #1E3A5F | Card borders, dividers |
| Border subtle | --border-subtle | rgba(255,255,255,0.06) | Faint separators |
| White overlay | --overlay-hover | rgba(255,255,255,0.04) | Hover state for rows |

Color hierarchy rule: Gold is reserved for the SINGLE most important action on any screen.

## 3. Typography Rules

Font stack:
- Display/Headlines: "Outfit", "Inter", system-ui, sans-serif
- Body/UI: "Inter", "Outfit", system-ui, sans-serif
- Data/Mono: "JetBrains Mono", "Fira Code", monospace — financial figures, HS codes, tracking numbers

| Level | Size | Weight | Line-height | Letter-spacing | Font | Usage |
|-------|------|--------|-------------|----------------|------|-------|
| Display XL | 56px | 700 | 1.05 | -2.5px | Outfit | Hero headlines only |
| Display | 40px | 700 | 1.1 | -1.8px | Outfit | Section headers |
| Heading 1 | 32px | 600 | 1.2 | -1.2px | Outfit | Page titles |
| Heading 2 | 24px | 600 | 1.25 | -0.8px | Outfit | Card titles |
| Heading 3 | 20px | 600 | 1.3 | -0.5px | Outfit | Widget headers |
| Heading 4 | 16px | 600 | 1.4 | -0.2px | Inter | Sidebar sections, labels |
| Body large | 16px | 400 | 1.6 | -0.1px | Inter | Intro text |
| Body | 14px | 400 | 1.6 | 0 | Inter | Default body |
| Body small | 13px | 400 | 1.5 | 0 | Inter | Dense UI, table cells |
| Caption | 12px | 500 | 1.4 | 0.2px | Inter | Labels, badges |
| Overline | 11px | 700 | 1.2 | 1.5px | Inter | Uppercase section labels |
| Data | 14px | 500 | 1.4 | 0 | JetBrains Mono | Prices, percentages, HS codes |
| Data large | 24px | 700 | 1.1 | -0.5px | JetBrains Mono | Dashboard KPIs, revenue |

Rules: headlines always negative letter-spacing; overlines always uppercase + tracked; financial data always monospace; never below 12px; max 3 font weights per component.

## 4. Component Styles

**Button — Primary (Gold CTA)**: bg `--accent-gold`, text `#0A1628`, padding `10px 20px`, radius `8px`, font `14px/600 Inter`, hover: brightness 1.1 + translateY(-1px) + shadow `0 4px 12px rgba(212,175,55,0.3)`, focus ring `2px gold` offset 2px, disabled opacity 0.4.

**Button — Secondary**: transparent bg, text `--text-primary`, border `1px solid --border-default`, radius `8px`, hover: bg `--overlay-hover`, border-color `--accent-gold-muted`.

**Button — Ghost**: transparent, text `--text-secondary`, padding `8px 12px`, radius `6px`, hover: text `--text-primary` + bg `--overlay-hover`.

**Card — Standard**: bg `--bg-surface`, border `1px solid --border-default`, radius `12px`, padding `24px`, no shadow; hover (if interactive): border-color `--accent-gold-muted`, translate(-1px).

**Card — Stat/KPI**: same as standard, structure = overline label + data-large value + caption delta (emerald `+` for positive, crimson `-` for negative).

**Input — Text**: bg `--bg-canvas`, border `1px solid --border-default`, radius `8px`, padding `10px 14px`, focus: border-color gold + ring `1px gold-faint`, error: border-color crimson.

**Table — Data**: header bg `--bg-raised`, `12px/500` uppercase tracked `--text-secondary`; row height `48px`, border-bottom subtle; row hover `--overlay-hover`; numbers in JetBrains Mono; selected row gold-faint bg + 2px gold left border.

**Badge/Tag**: padding `2px 8px`, radius `4px`, `11px/600` uppercase tracked. Variants: success (emerald), danger (crimson), warning (amber), info (azure), gold, neutral.

**Navigation — Sidebar**: width 260px (collapsed 64px), bg `--bg-surface`, border-right `--border-default`; active item: gold-faint bg + gold text + 2px gold left border; hover: `--overlay-hover`.

**Modal/Dialog**: bg `--bg-raised`, border `--border-default`, radius `16px`, shadow `0 24px 48px rgba(0,0,0,0.5)`, max-width 480/640/960px, padding `32px`, backdrop `rgba(10,22,40,0.8)` + blur(4px).

## 5. Layout Principles

Base unit: 4px. Spacing scale: 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96, 128.

| Context | Spacing |
|---------|---------|
| Inline elements (icon + text) | 8px |
| Related items in a group | 12px |
| Between form fields | 16px |
| Between card sections | 20-24px |
| Between cards in a grid | 16-24px |
| Between page sections | 64-96px |
| Page top/bottom padding | 32-48px |

Grid: Dashboard = 12-column, 24px gutter. Marketing = max-width 1200px centered. Content = max-width 720px. Full-bleed = 100vw with inner container.

Border-radius scale: badge/tag 4px, button/input 8px, card 12px, modal 16px, avatar/toggle 9999px.

Whitespace philosophy: structural, not decorative — groups related content and creates hierarchy.

## 6. Depth & Elevation

Border-first depth system on dark backgrounds:

| Level | Surface | Border | Shadow | Usage |
|-------|---------|--------|--------|-------|
| 0 | --bg-canvas #0A1628 | none | none | Page background |
| 1 | --bg-surface #0F1D32 | --border-default | none | Cards, sidebar, panels |
| 2 | --bg-raised #162440 | --border-default | 0 4px 16px rgba(0,0,0,0.4) | Dropdowns, popovers |
| 3 | #1C2E52 | --border-default | 0 16px 48px rgba(0,0,0,0.6) | Modals, overlays |
| Overlay | rgba(10,22,40,0.8) | none | none | Backdrop behind modals |

Rule: each level ≈ +5 lightness in the navy spectrum; never jump more than 2 levels at once.

## 7. Do's and Don'ts

**DO**: use gold sparingly (one gold CTA per viewport); use borders for depth on dark backgrounds; keep financial data in monospace always; negative letter-spacing on headlines; overline labels above KPI values; emerald=profit/crimson=loss consistently; 150ms ease transitions; backdrop-blur for overlays.

**DON'T**: gradients on backgrounds; pure white (#FFFFFF) text — use #F1F5F9; pure black (#000000) — darkest surface is #0A1628; gold text on gold bg; center-align body text; rounded-full buttons; mix warm/cool grays; >3 font weights per component; generic stock photos; AI slop patterns (gradient heroes, 3-col icon grids, uniform card heights).

**ABSOLUTE NEVERS**: decorative fonts (Comic Sans, Papyrus); rainbow color coding; critical financial data below the fold; unanimated number changes; light mode as default.

## 8. Responsive Behavior

| Breakpoint | Width | Layout Changes |
|------------|-------|----------------|
| Mobile | <640px | Single column, sidebar becomes bottom tab bar, KPI cards stack |
| Tablet | 640-1024px | 2-column grids, collapsible sidebar |
| Desktop | 1024-1440px | Full 12-column grid, persistent sidebar |
| Wide | >1440px | Content max-width 1440px centered |

Touch targets: minimum 44x44px. Mobile: bottom tab bar (5 icons max), swipe between sections, pull-to-refresh, sticky table headers with horizontal scroll.

Font scaling: body stays 14px on all breakpoints; Display XL → 36px mobile, Display → 28px, H1 → 24px.

## 9. Agent Prompt Guide

**Quick Palette**: Canvas #0A1628, Surface #0F1D32, Raised #162440, Gold #D4AF37, Emerald #10B981, Crimson #EF4444, Azure #3B82F6, Amber #F59E0B, Text #F1F5F9, Muted #94A3B8, Faint #64748B, Border #1E3A5F. Fonts: Outfit (display), Inter (body), JetBrains Mono (data).

**Dashboard page**: "Build a GeoTrading dashboard. Dark navy canvas (#0A1628). Top row: 4 KPI cards (Revenue, Active Trades, AI Modules, Markets) with overline label + monospace value + delta badge. Below: trade pipeline table (left) + revenue chart (right). Sidebar nav with gold active state. Outfit headings, JetBrains Mono numbers."

**Landing page**: "Build a GeoTrading landing page. Full-bleed dark navy hero, 56px Outfit headline (-2.5px tracking), gold CTA. Asymmetric feature grid (not 3-column icons). Stats section with counters. Emerald for growth metrics. 4-column footer."

**Trading view**: "Build a trade line overview table: Trade Line, Region, Markup %, Volume, Status. Monospace numbers. 4% white overlay row hover. Status badges: Active (emerald), Pending (amber), Paused (neutral). Selected row: gold left border + gold-faint bg."

**Vehicle export catalog**: "Build a vehicle catalog page. Large hero image with overlay text. Grid of vehicle cards: full-bleed photo top, specs below in monospace. Filter bar with category tags. Gold 'Request Quote' CTA per card. No gradients, no rounded-full."

**CRM contact view**: "Build a GoHighLevel-style contact detail page. Left panel: avatar, name, tags, contact info. Right panel: tabbed (Activity, Notes, Deals, Tasks). Timeline for activities. Gold accent on primary action. Phone numbers in monospace."

**Invoice generator**: "Build a professional invoice. Header: GeoTrading logo + gold horizontal rule. Bill-to in Outfit heading. Line items in clean data table with alternating subtle rows. Totals right-aligned in JetBrains Mono. Footer: UBA/CBAO banking details. Print-optimized A4."

**GeoTrading Brand**: Company GeoTrading General Trading LLC, Parent Gomale Group, Tagline "Trade Beyond Borders", Markets UAE/Côte d'Ivoire/Senegal/Congo-RDC/Crypto, Divisions AI Services | Physical Trading | Algorithmic Trading | Business Assistant, Logo: stylized globe with gold meridian lines on navy.

## Light Mode Override (optional, not default)

| Token | Dark (default) | Light |
|-------|---------------|-------|
| Canvas | #0A1628 | #F8FAFC |
| Surface | #0F1D32 | #FFFFFF |
| Raised | #162440 | #F1F5F9 |
| Text primary | #F1F5F9 | #0F172A |
| Text secondary | #94A3B8 | #64748B |
| Border | #1E3A5F | #E2E8F0 |
| Gold accent | #D4AF37 | #B8962E |

Rule: light mode keeps the same spacing/typography/components — only colors change. Never redesign layout for light mode.
