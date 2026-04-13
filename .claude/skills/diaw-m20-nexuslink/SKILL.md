---
name: diaw-m20-nexuslink
description: >
  NEXUS-LINK: AI-powered integration hub module. Connects all DIAW modules with
  external systems via API, webhook, and MCP integrations. Builds custom
  connectors, data pipelines, ETL workflows, and integration architectures.
  Handles Zapier/Make/n8n equivalent workflows natively. Activates on
  NEXUS-LINK, integration, API connector, webhook, data pipeline, ETL,
  workflow automation, Zapier, Make, n8n, third-party integration.
user-invocable: true
context: fork
effort: high
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - WebSearch
  - mcp__ruflo__*
  - mcp__github__*
---

# NEXUS-LINK: Integration Hub Module v3.0

## Agent Swarm Configuration
- **Topology**: Pipeline | **Max Agents**: 4 | **Quality Gate**: 0.97
- **Agents**: Integration Architect, Connector Agent, Data Agent, Monitor Agent

## Integration Capabilities

### Pre-Built Connectors Library
| Category | Integrations |
|----------|-------------|
| CRM | Salesforce, HubSpot, Zoho CRM, Pipedrive |
| ERP | SAP, Oracle NetSuite, Microsoft Dynamics, Odoo |
| Accounting | QuickBooks, Xero, Sage, Zoho Books |
| E-commerce | Shopify, WooCommerce, Magento, BigCommerce |
| Marketing | Mailchimp, Klaviyo, ActiveCampaign, Brevo |
| Analytics | GA4, Mixpanel, Amplitude, Heap |
| Communication | Slack, Teams, WhatsApp Business, Telegram |
| Project Mgmt | Jira, Linear, Asana, Monday.com, Notion |
| Payments | Stripe, PayTabs, Network International, Tabby |
| HR | Workday, BambooHR, Darwinbox, HRMS |
| Support | Zendesk, Intercom, Freshdesk |
| Storage | AWS S3, Google Cloud Storage, Dropbox, SharePoint |

### Integration Patterns

**1. Real-Time Webhooks**
```python
# Webhook endpoint that triggers DIAW workflows
@app.post("/webhooks/diaw/{module}")
async def handle_webhook(module: str, payload: dict, background_tasks: BackgroundTasks):
    """
    Receive events from external systems and trigger DIAW module actions.
    Supports: Stripe payments → FINOVA, GitHub PRs → AEGIS-PRIME,
              HubSpot deals → diaw-sales, GA4 events → GROWTH-ENGINE
    """
    validated = validate_webhook_signature(payload, request.headers)
    background_tasks.add_task(route_to_module, module, validated)
    return {"status": "accepted", "job_id": generate_job_id()}
```

**2. Scheduled ETL Pipelines**
```yaml
# Daily data sync pipeline
pipeline:
  name: crm-to-analytics-sync
  schedule: "0 2 * * *"  # 2 AM daily
  steps:
    - extract:
        source: salesforce
        objects: [Lead, Opportunity, Account, Contact]
        incremental: true
        watermark: last_modified_date
    - transform:
        normalize_fields: true
        deduplicate: true
        enrich:
          - company_data: clearbit
          - firmographics: apollo
    - load:
        destination: bigquery
        dataset: diaw_crm
        mode: upsert
```

**3. Event-Driven Workflows**
```
Trigger: New customer signs up (Stripe webhook)
  → NEXUS-LINK receives event
  → Enriches with company data (Clearbit/Apollo)
  → Creates deal in CRM (HubSpot)
  → Sends Slack notification to sales team
  → Starts onboarding email sequence (Klaviyo)
  → Creates Linear ticket for CS team
  → Logs to analytics (Mixpanel event)
  → Updates financial forecast (FINOVA)
```

### Custom Workflow Builder
```javascript
// Low-code workflow definition
const workflow = {
  name: "lead-to-revenue",
  trigger: { type: "webhook", source: "website_form" },
  steps: [
    { action: "enrich_lead", tool: "apollo" },
    { action: "score_lead", tool: "diaw-sales", threshold: 65 },
    { condition: "score >= 65",
      then: [
        { action: "create_deal", tool: "hubspot" },
        { action: "notify_sales", tool: "slack" },
        { action: "start_sequence", tool: "diaw-sales", sequence: "hot-lead" }
      ],
      else: [
        { action: "add_to_nurture", tool: "klaviyo", list: "cold-leads" }
      ]
    }
  ]
};
```

### Data Pipeline Monitoring
| Metric | Target | Alert |
|--------|--------|-------|
| Pipeline success rate | >99% | <97% |
| Average latency | <5s | >30s |
| Data freshness | <15 min | >1 hour |
| Error rate | <0.1% | >1% |
| Records processed | Track daily volume | -20% drop |

### UAE/MENA System Integrations
- **Tasheel**: UAE government services integration
- **Bayanat**: Abu Dhabi data platform
- **Dubai Pulse**: Dubai government data APIs
- **TAMM**: Abu Dhabi service platform
- **DubaiNow**: Dubai app integrations

## Revenue Model
- **Subscription**: $200/mo
- **Connector Setup**: $500-$2,000 per custom connector
- **Data Volume**: $0.001 per 1,000 records after 1M/mo
- **Credits**: 15-50 per integration workflow

## Example Invocations
- "NEXUS-LINK: Connect our Shopify store to HubSpot CRM with lead enrichment"
- "Build a data pipeline from Salesforce to BigQuery for our analytics dashboard"
- "NEXUS-LINK: Create a webhook workflow that automatically qualifies leads from our website"
