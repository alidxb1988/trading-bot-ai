---
name: gohighlevel-mcp-setup
description: Set up and configure GoHighLevel MCP server connection for Claude Code. Use when user asks to connect GoHighLevel, setup GHL, configure CRM, install GoHighLevel MCP, or troubleshoot MCP connection issues.
metadata:
  author: Diaw Trading
  version: 1.0.0
---

# GoHighLevel MCP Setup

## Option A: Official MCP Server (Quickest)

**Step 1: Create Private Integration in GoHighLevel**
1. Log into GoHighLevel
2. Navigate to Settings > Private Integrations > Create New Integration
3. Name it "Claude Code MCP"

**Step 2: Set Permissions**
Start with minimum: View Locations, View/Edit Contacts, View Pipelines, Edit Calendars, View Conversations, View/Edit Tags, View Custom Fields

**Step 3: Copy PIT Token + Location ID**
- Copy the Private Integration Token immediately (shown only once)
- Copy Location ID from Settings > Business Profile

**Step 4: Add MCP Config** — add to `~/.claude/mcp.json`:
```json
{
  "mcpServers": {
    "gohighlevel": {
      "url": "https://services.leadconnectorhq.com/mcp/",
      "headers": {
        "Authorization": "Bearer YOUR_PIT_TOKEN",
        "Version": "2021-07-28"
      }
    }
  }
}
```

**Step 5: Restart Claude Code and test**
- "How many contacts do I have in GoHighLevel?"
- "Show me my active pipeline stages"

## Option B: Community Server (269+ Tools)
```bash
git clone https://github.com/mastanley13/GoHighLevel-MCP.git
cd GoHighLevel-MCP
npm install
cp .env.example .env
# Edit .env: GHL_API_KEY, GHL_BASE_URL, GHL_LOCATION_ID
npm run build
npm start
```

Add to `~/.claude/mcp.json`:
```json
{
  "mcpServers": {
    "ghl-mcp-server": {
      "command": "node",
      "args": ["path/to/GoHighLevel-MCP/dist/server.js"],
      "env": {
        "GHL_API_KEY": "your_private_integrations_api_key",
        "GHL_BASE_URL": "https://services.leadconnectorhq.com",
        "GHL_LOCATION_ID": "your_location_id"
      }
    }
  }
}
```

## Troubleshooting

- **Cannot see GHL data**: Verify PIT token correct/not expired, confirm Location ID matches sub-account, restart Claude Code after config change
- **401 Errors**: Token expired — create new Private Integration
- **Can read but cannot update**: Permissions set to View only — enable Edit
- **MCP server not appearing**: Check JSON syntax with a validator
