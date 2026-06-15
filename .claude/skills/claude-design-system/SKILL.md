---
name: claude-design-system
description: Transform Claude from AI slop into a world-class designer using DESIGN.md systems. Use when user asks for website/UI design, landing pages, dashboards, or mentions DESIGN.md, design systems, or wants to avoid generic AI-generated layouts. 5-step workflow: pick format -> add integrations -> reference materials -> first generation -> refine and codify.
metadata:
  author: Diaw Trading (adapted from VoltAgent / Jack Roberts methodology)
  version: 2.0.0
  source_repo: https://github.com/VoltAgent/awesome-design-md
---

# Claude Design System Skill

## Purpose
Eliminate "AI slop" — generic gradient heroes, 3-column icon grids, blue/gray palettes, uniform border-radius. Make Claude design like Stripe, Apple, Vercel, or any world-class brand by reading a DESIGN.md file before generating UI.

## The 5-Step Design Workflow

**Step 1 — Pick Your Format**
Choose a DESIGN.md from the design library (`design-library/sites/`) matching the desired aesthetic, or use the custom GeoTrading/Diaw Trading systems in `custom/`.

| Category | Best For | Examples |
|----------|----------|---------|
| AI/LLM Platforms | AI products, dashboards | Claude, Mistral, ElevenLabs |
| Developer Tools | Dev tools, SaaS | Vercel, Cursor, Raycast |
| Fintech | Payment, banking, crypto | Stripe, Coinbase, Revolut, Wise |
| E-commerce | Retail, marketplace | Nike, Shopify, Airbnb |
| Automotive | Luxury, premium | Tesla, Ferrari, Lamborghini, BMW |
| Media | Content, editorial | Spotify, WIRED, The Verge |
| Productivity | SaaS, workspace | Linear, Notion, Cal.com |

Clone the library for offline access:
```bash
git clone --depth 1 https://github.com/VoltAgent/awesome-design-md.git \
  .claude/skills/claude-design-system/design-library
```

**Step 2 — Add Your Integrations**
- Firecrawl MCP — scrape any website's design for reference
- Browser MCP — screenshot reference designs
- Kie / Higgsfield — AI image/video generation for hero sections
- Godly.website — browse curated design inspiration

**Step 3 — Reference Materials**
Gather 2-3 reference sites, scrape with Firecrawl, screenshot key sections, feed to Claude alongside the chosen DESIGN.md.

**Step 4 — First Generation**
```
Read the DESIGN.md file in my project root. Now build a [page] for
[product]. Use the visual language defined in DESIGN.md. Reference
the screenshots provided for layout inspiration. Do NOT default to
generic AI patterns -- follow the design system strictly.
```

**Step 5 — Refine and Codify**
Review output, request specific (not vague) changes, save the final DESIGN.md as the permanent brand system, and reference it from `CLAUDE.md`.

## DESIGN.md Format (9 Sections)

| # | Section | Captures |
|---|---------|----------|
| 1 | Visual Theme & Atmosphere | Mood, density, design philosophy |
| 2 | Color Palette & Roles | Semantic name + hex + functional role |
| 3 | Typography Rules | Font families, full hierarchy table |
| 4 | Component Stylings | Buttons, cards, inputs, nav — with states |
| 5 | Layout Principles | Spacing scale, grid, whitespace philosophy |
| 6 | Depth & Elevation | Shadow system, surface hierarchy |
| 7 | Do's and Don'ts | Design guardrails and anti-patterns |
| 8 | Responsive Behavior | Breakpoints, touch targets, collapsing strategy |
| 9 | Agent Prompt Guide | Quick color reference, ready-to-use prompts |

## AI Slop Detection Checklist

Before shipping ANY design, check for these red flags:
- [ ] Generic gradient hero section
- [ ] 3-column icon grid with equal spacing
- [ ] Default blue/gray color palette
- [ ] Uniform border-radius on all elements
- [ ] "Clean, modern UI" with no distinctive character
- [ ] Stock-photo-looking AI-generated images
- [ ] Centered everything (no asymmetry)
- [ ] Same font weight throughout
- [ ] No hover/focus states defined
- [ ] Missing dark mode consideration

If 3+ are checked → redesign using the DESIGN.md system.

## Anti-Slop Principles
1. Every element earns its pixel
2. Typography creates hierarchy (2-3 font families with purpose)
3. Color tells a story (max 5 colors + neutrals, semantic roles)
4. Asymmetry over symmetry
5. Animations serve comprehension, not decoration
6. Whitespace is structural
7. Dark mode is a separate design language, not inverted colors
8. Mobile-first, then enhance
9. Micro-interactions signal quality
10. Test at 3 viewports minimum (375px, 768px, 1440px)

## Quick-Start Commands

**Use a pre-built DESIGN.md**
"Apply the Stripe design system to my project. Copy sites/stripe/DESIGN.md from the design library to my project root."

**Build from reference**
"Scrape vercel.com with Firecrawl, extract design tokens, create a DESIGN.md inspired by Vercel adapted for my brand colors."

**Build from scratch**
"Create a DESIGN.md for [product]. Brand personality: [bold/minimal/playful/premium]. Primary color: [hex]. Follow the 9-section format."

**Audit existing design**
"Review my current site against the AI Slop Detection Checklist. Score each item, then suggest improvements using my DESIGN.md."

## GeoTrading / Diaw Trading Custom Systems

- `custom/GEOTRADING-DESIGN.md` — Dark-sovereign navy/gold/emerald system for GeoTrading General Trading LLC (dashboards, trading views, vehicle export catalog)
- `custom/DIAW-TRADING-DESIGN.md` — Inherits GeoTrading system with West African warmth (terracotta accent) for Diaw Trading Import-Export

## Integration with Other Skills

| Workflow | Skills Chain |
|----------|-------------|
| New website | claude-design-system → google-stitch-design → remotion-video |
| Client project | claude-design-system → gohighlevel-crm |
| E-commerce | claude-design-system → ecommerce-operations → gohighlevel-crm |

## Key URLs

| Resource | URL |
|----------|-----|
| awesome-design-md Repo | https://github.com/VoltAgent/awesome-design-md |
| Google Stitch (DESIGN.md origin) | https://stitch.withgoogle.com |
| Firecrawl MCP | https://www.firecrawl.dev |
| Godly Design Inspiration | https://godly.website |
