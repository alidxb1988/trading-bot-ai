---
name: gohighlevel-crm
description: Full GoHighLevel CRM automation via MCP. Use when user asks to manage contacts, pipelines, appointments, conversations, invoices, products, social media, blogs, email campaigns, payments, or any CRM operations. Triggers on "GoHighLevel", "GHL", "CRM", "leads", "pipeline", "contacts", "appointments", "invoice", "follow-up", "SMS", "email campaign", "social media post", "coupon", "order", "subscription", "blog post".
license: MIT
metadata:
  author: Diaw Trading
  version: 1.0.0
  mcp-server: gohighlevel
  github-community: https://github.com/mastanley13/GoHighLevel-MCP
---

# GoHighLevel CRM Automation

Complete AI-powered CRM management through GoHighLevel's MCP server. 269+ tools across 19 categories.

## When to Use

- Managing contacts, leads, or customer data
- Pipeline reviews and opportunity tracking
- Scheduling appointments and calendar management
- Sending SMS, email, or managing conversations
- Creating invoices, estimates, and processing payments
- Managing products, inventory, and e-commerce orders
- Social media scheduling and blog management
- Generating CRM reports and analytics
- Automating follow-up sequences
- Cleaning and deduplicating contact data

## Prerequisites

- GoHighLevel account (any plan)
- Private Integration Token (PIT) configured in MCP — see `gohighlevel-mcp-setup` skill
- Location ID from GHL Settings > Business Profile

## Core Tool Categories (269 tools)

- **Contact Management (31)**: create/search/update/delete contacts, tags, tasks, notes, workflow membership, followers
- **Messaging & Conversations (20)**: send_sms, send_email, conversations, recordings, transcriptions
- **Opportunity & Pipeline (10)**: search_opportunities, get_pipelines, create/update/delete opportunity, followers
- **Calendar & Appointments (14)**: calendars, free slots, appointments, block slots
- **Email Marketing (5)**: campaigns, templates
- **Location Management (24)**: locations, tags, custom fields/values, templates, timezones
- **Social Media (17)**: posts, accounts, OAuth, CSV bulk upload, categories/tags
- **Blog Management (7)**: posts, sites, authors, categories, slug check
- **Media Library (3)**: get/upload/delete media files
- **Custom Objects (9)**: schemas and records, search
- **Associations (10)**: object relationships
- **Custom Fields V2 (8)**: field & folder CRUD
- **Workflows (1)**: list workflows
- **Surveys (2)**: surveys & submissions
- **Store Management (18)**: shipping zones/rates, carriers, store settings
- **Products (10)**: products, prices, inventory, collections
- **Payments (20)**: providers, orders, transactions, subscriptions, coupons
- **Invoices & Billing (39)**: templates, recurring invoices, invoices, estimates
- **Email Verification (1)**: verify_email

See `references/workflows.md` for pre-built workflow prompts.
