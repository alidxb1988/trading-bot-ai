---
name: diaw-m07-tradeflow
description: >
  TRADE-FLOW: AI-powered trade and logistics module. Handles supply chain
  optimization, freight booking, customs documentation, shipment tracking,
  warehouse management, import/export compliance, and UAE free zone operations.
  Activates on TRADE-FLOW, trade, logistics, supply chain, freight, customs,
  shipment, warehouse, import, export, free zone.
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
---

# TRADE-FLOW: Trade & Logistics Module v3.0

## Agent Swarm Configuration
- **Topology**: Pipeline | **Max Agents**: 4 | **Quality Gate**: 0.95
- **Agents**: Trade Coordinator, Documentation Agent, Tracking Agent, Compliance Agent

## Core Capabilities

### Supply Chain Optimization
- Multi-modal freight comparison (air, sea, road, rail)
- Route optimization with cost/time trade-off analysis
- Supplier risk assessment and diversification recommendations
- Lead time prediction using historical data and market signals
- Safety stock calculations and reorder point optimization

### UAE/MENA Trade Operations
- **Free Zone Expertise**: JAFZA, DAFZA, DMCC, ADGM, Dubai Airport Free Zone
- **Customs Documentation**: Commercial invoice, packing list, bill of lading, COO
- **UAE Import Rules**: Restricted goods list, Halal certification, ESMA standards
- **VAT on Imports**: Customs duty + 5% VAT calculation and filing
- **Incoterms**: Automated Incoterms selection based on buyer/seller risk preference

### Automation Workflows
```
Order Received → Freight Quote Comparison (3 carriers) → Booking → 
  Documentation Generation → Customs Pre-clearance → 
  Tracking Setup → Milestone Notifications → 
  Delivery Confirmation → Invoice + POD
```

### Platform Integrations
| System | Integration |
|--------|------------|
| Freight Forwarders | DHL, FedEx, Aramex, CEVA, DB Schenker APIs |
| Customs | UAE Customs digital gateway |
| ERP | SAP, Oracle, NetSuite connectors |
| WMS | Warehouse management via RFID/barcode |
| Port Authority | DP World, AD Ports real-time data |

### Document Generation
- Commercial Invoice (UAE and international format)
- Certificate of Origin (CoO) with Chamber of Commerce stamp prep
- Dangerous Goods Declaration (DGD)
- Packing List with weights and dimensions
- Letter of Credit documentation support

## Revenue Model
- **Subscription**: $250/mo
- **Per-Shipment Fee**: $10-$50 per shipment processed
- **Consulting**: $200/hr for trade compliance
- **Credits**: 20-60 per logistics setup

## Example Invocations
- "TRADE-FLOW: Compare freight quotes for 5 FCL containers from Shanghai to Jebel Ali"
- "Generate customs documentation for importing electronics through JAFZA free zone"
- "TRADE-FLOW: Optimize our supply chain to reduce lead times by 30%"
