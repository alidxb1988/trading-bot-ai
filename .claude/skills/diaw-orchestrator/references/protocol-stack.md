# DIAW Protocol Stack v3.0

## Layer 1: MCP (Model Context Protocol)

### Available MCP Servers
```yaml
mcp_servers:
  ruflo:
    description: Agent orchestration via RuFlow
    tools: [spawn_swarm, coordinate_agents, monitor_progress, get_results]
    auth: API key in ANTHROPIC_API_KEY

  github:
    description: Repository management
    tools: [create_repo, push_code, create_pr, manage_issues, get_file]
    auth: GITHUB_TOKEN

  stripe:
    description: Payment processing
    tools: [create_customer, create_subscription, generate_invoice, process_payment]
    auth: STRIPE_SECRET_KEY

  firecrawl:
    description: Web scraping and market intelligence
    tools: [scrape_url, search_web, crawl_site, extract_data]
    auth: FIRECRAWL_API_KEY

  analytics:
    description: Business analytics
    tools: [get_metrics, create_report, track_event, get_cohort]
    auth: ANALYTICS_API_KEY

  slack:
    description: Team communication
    tools: [send_message, create_channel, post_to_channel, get_messages]
    auth: SLACK_BOT_TOKEN

  linear:
    description: Project management
    tools: [create_issue, update_status, get_sprint, create_project]
    auth: LINEAR_API_KEY
```

## Layer 2: A2A (Agent-to-Agent Protocol)

### Agent Card Template (Published by each DIAW Module)
```json
{
  "name": "DIAW-{MODULE_NAME}",
  "version": "3.0.0",
  "description": "DIAW Trading {module} specialist agent",
  "url": "https://api.diawtrading.com/agents/{module}",
  "capabilities": {
    "streaming": true,
    "pushNotifications": true,
    "stateTransitionHistory": true
  },
  "skills": [
    {
      "id": "primary_skill",
      "name": "Primary Skill Name",
      "description": "What this agent can do",
      "tags": ["keyword1", "keyword2"]
    }
  ],
  "authentication": {
    "schemes": ["bearer", "apiKey"]
  }
}
```

### A2A Task Lifecycle
```
SUBMITTED → WORKING → (INPUT_REQUIRED?) → COMPLETED | FAILED | CANCELLED
```

## Layer 3: ACP (Agent Communication Protocol)

### Communication Patterns
```python
# 1. Request-Response (synchronous)
result = await agent.execute(task="research_prospect", params={"company": "Acme"})

# 2. Publish-Subscribe (event-driven)
await broker.publish(topic="new_lead", data={"score": 85, "company": "Acme"})
await broker.subscribe(topic="new_lead", handler=sales_agent.handle_lead)

# 3. Streaming (real-time)
async for chunk in agent.stream(task="generate_report"):
    yield chunk

# 4. Multimodal (text + files)
result = await agent.execute(
    task="analyze_document",
    inputs={"text": "...", "file": pdf_bytes, "image": screenshot_bytes}
)
```
