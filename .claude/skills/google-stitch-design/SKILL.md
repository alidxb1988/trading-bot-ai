---
name: google-stitch-design
description: Generate UI designs, multi-page websites, React components, and design systems using Google Stitch AI. Use when user asks to design a UI, create a landing page, generate a website mockup, build React components, create a design system, or convert designs to code.
metadata:
  author: google-labs-code
  version: 1.0.0
  github-skills: https://github.com/google-labs-code/stitch-skills
  github-sdk: https://github.com/google-labs-code/stitch-sdk
  docs: https://stitch.withgoogle.com
---

# Google Stitch Design

## Installation
```bash
npx skills add google-labs-code/stitch-skills --skill stitch-design --global
npx skills add google-labs-code/stitch-skills --skill stitch-loop --global
npx skills add google-labs-code/stitch-skills --skill design-md --global
npx skills add google-labs-code/stitch-skills --skill enhance-prompt --global
npx skills add google-labs-code/stitch-skills --skill react:components --global
npx skills add google-labs-code/stitch-skills --skill remotion --global
npx skills add google-labs-code/stitch-skills --skill shadcn-ui --global
npm install @google/stitch-sdk
```

## API Key Setup
```bash
export STITCH_API_KEY="your-api-key"
```
Get key from: https://stitch.withgoogle.com/docs/mcp/setup/

## MCP Configuration
Add to `~/.claude/mcp.json`:
```json
{
  "mcpServers": {
    "stitch": {
      "command": "npx",
      "args": ["-y", "@google/stitch-sdk", "mcp"],
      "env": { "STITCH_API_KEY": "your-api-key" }
    }
  }
}
```

## MCP Tools
- `create_project` — New design project
- `generate_screen_from_text` — AI screen generation
- `edit_screen` — Modify existing screens
- `generate_variants` — Create design variants
- `get_screen` / `list_screens` / `list_projects`
- `create_design_system` / `list_design_systems` / `apply_design_system`

## Capabilities
- UI generation from text descriptions, multi-screen website/app design
- Interactive prototyping, design system creation (DESIGN.md)
- Code export: React, shadcn-ui, HTML, screenshots
- Remotion video generation from designs
- Device types: mobile, tablet, desktop, agnostic
- Creative range: REFINE → EXPLORE → REIMAGINE
- Limits: 350 monthly generations (free tier)
