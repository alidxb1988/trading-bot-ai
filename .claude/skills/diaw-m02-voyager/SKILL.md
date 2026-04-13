---
name: diaw-m02-voyager
description: >
  VOYAGER: AI-powered travel technology module. Builds travel booking platforms,
  itinerary planners, hotel/flight aggregators, tour management systems, and
  travel agency automation. Handles pricing optimization, dynamic packaging,
  loyalty programs, and multilingual support. Activates on VOYAGER, travel,
  travel tech, booking platform, itinerary, hotel, flight, tour, travel agency.
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
  - mcp__firecrawl__*
  - mcp__stripe__*
---

# VOYAGER: Travel Tech Module v3.0

## Agent Swarm Configuration
- **Topology**: Hierarchical | **Max Agents**: 5 | **Quality Gate**: 0.95
- **Agents**: Travel Coordinator, Booking Engine Agent, Content Agent, Pricing Agent, UX Agent

## Core Capabilities

### Platform Types
- **OTA (Online Travel Agency)**: Full booking platform with inventory aggregation
- **Tour Operator**: Custom itinerary builder, group management, guide coordination
- **Hotel Management**: Property listing, availability calendar, rate management
- **Travel Agency CRM**: Client profiles, trip history, automated follow-ups

### Key Features
- Dynamic pricing engine (demand-based, seasonal, competitor-aware)
- Multi-currency + multi-language support (Arabic, English, French)
- Real-time availability sync with GDS (Amadeus, Sabre, Travelport)
- AI-powered itinerary recommendations based on traveler profile
- Loyalty program management with points/rewards engine
- Automated visa requirement checker for UAE/GCC travelers

### UAE Travel Market Focus
- Inbound tourism: Dubai, Abu Dhabi, Ras Al Khaimah packages
- Outbound: Popular destinations for UAE residents (Maldives, Europe, Asia)
- MICE (Meetings, Incentives, Conferences, Exhibitions) segment
- Arabic content and RTL interface support
- Integration with UAE tourism authority APIs

## Revenue Model
- **Subscription**: $220/mo base
- **Booking Commission**: 5-15% per completed booking
- **White-label License**: $5,000-$20,000 setup + $500/mo
- **Credits**: 20-60 per platform build

## Example Invocations
- "VOYAGER: Build a travel booking platform for UAE-to-Maldives packages"
- "Create an AI itinerary planner for adventure travelers visiting Oman"
- "VOYAGER: Automate booking confirmations and travel document delivery for a tour operator"
