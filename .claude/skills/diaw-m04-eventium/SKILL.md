---
name: diaw-m04-eventium
description: >
  EVENTIUM: AI-powered events management module. Handles event planning,
  ticketing systems, attendee management, venue coordination, sponsor management,
  live streaming integration, post-event analytics, and automated follow-ups.
  Specializes in UAE/MENA corporate events, conferences, and exhibitions.
  Activates on EVENTIUM, event, conference, exhibition, ticketing, venue, MICE.
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
  - mcp__stripe__*
---

# EVENTIUM: Events Management Module v3.0

## Agent Swarm Configuration
- **Topology**: Hierarchical | **Max Agents**: 4 | **Quality Gate**: 0.95
- **Agents**: Events Coordinator, Ticketing Agent, Content Agent, Analytics Agent

## Core Capabilities

### Event Types Supported
- Corporate conferences and seminars (50-5,000 attendees)
- Trade exhibitions and expos (GITEX, Arab Health, Cityscape style)
- Product launches and press events
- Networking events and meetups
- Virtual and hybrid events with live streaming
- Awards ceremonies and gala dinners

### Platform Features
- **Registration & Ticketing**: Multi-tier pricing (Early Bird, Standard, VIP, Group)
- **Attendee Management**: Profile management, networking matchmaking, schedules
- **Sponsor Portal**: Tier management (Platinum/Gold/Silver), logo placement, lead capture
- **Mobile App**: Event guide, session schedules, speaker profiles, networking
- **Live Streaming**: Zoom/Teams integration, recording, replay access
- **Analytics**: Registration conversion, attendance, engagement, ROI report

### UAE/MENA Specializations
- Arabic content and RTL interface
- UAE public holiday awareness for scheduling
- Local vendor and venue database (Dubai, Abu Dhabi, Sharjah)
- VAT compliance (5% UAE VAT on ticket prices)
- Integration with Dubai Tourism and DIFC event permits

### Automation Workflows
```
Pre-Event:  Registration → Confirmation email → Calendar invite → Reminder sequence
Day-of:     QR code check-in → Badge printing → Live updates → Session reminders
Post-Event: Thank you email → Survey → Recording links → Certificate delivery → Follow-up
```

## Revenue Model
- **Subscription**: $140/mo
- **Per-Event Fee**: $500-$5,000 depending on scale
- **Ticketing Commission**: 2-3% of ticket sales
- **Credits**: 15-45 per event setup

## Example Invocations
- "EVENTIUM: Set up a 500-person tech conference ticketing system with VIP tiers"
- "Create an automated post-event follow-up sequence for leads generated at GITEX"
- "EVENTIUM: Build a hybrid event platform with live streaming and virtual networking"
