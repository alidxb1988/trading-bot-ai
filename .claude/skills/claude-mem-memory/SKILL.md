---
name: claude-mem-memory
description: Persistent cross-session memory for Claude using SQLite-FTS5 and Chroma vector search. Use when user asks about remembering context, storing decisions, recalling past conversations, or setting up persistent memory.
metadata:
  author: thedotmack
  version: 1.0.0
  github: https://github.com/thedotmack/claude-mem
---

# Claude-Mem Persistent Memory

## Installation
```bash
npx claude-mem install
```

## Features
- Automatic decision and tool-call capture across sessions
- 3-layer token-efficient retrieval: search → timeline → get_observations
- ~10x token savings by filtering before fetching (95% lower consumption per session)
- SQLite-FTS5 full-text search + Chroma hybrid semantic/keyword search
- MCP search tools: search, timeline, get_observations, status
- Real-time web UI at http://localhost:37777 (SSE, infinite scroll)
- Multilingual support (28 languages, incl. French for OHADA contracts)
- Privacy tags for sensitive data (banking, contracts)
- Folder-level CLAUDE.md context injection
- 5 lifecycle hooks: SessionStart, UserPromptSubmit, PostToolUse, Stop, SessionEnd

## Search Workflow
```
Step 1: search(query="authentication bug", type="bugfix", limit=10)
Step 2: Review index, identify relevant IDs
Step 3: get_observations(ids=[123, 456])
```

## Integration with Diaw Trading
- Store supplier contacts and deal terms
- Remember HS codes used for recurring products
- Track shipment histories and customs decisions
- Maintain client preference profiles across sessions

## System Requirements
- Node.js 18.0.0+, Bun (auto-installed), uv for vector search (auto-installed)
