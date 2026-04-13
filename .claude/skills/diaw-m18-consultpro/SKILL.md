---
name: diaw-m18-consultpro
description: >
  CONSULT-PRO: AI-powered business consulting module. Delivers management
  consulting services including business diagnostics, process improvement,
  organizational restructuring, digital transformation roadmaps, and
  implementation support. Follows McKinsey, BCG, and Bain methodologies.
  Activates on CONSULT-PRO, consulting, business diagnostic, process improvement,
  digital transformation, organizational design, management consulting.
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

# CONSULT-PRO: Business Consulting Module v3.0

## Agent Swarm Configuration
- **Topology**: Expert Panel | **Max Agents**: 4 | **Quality Gate**: 0.96
- **Agents**: Senior Consultant, Industry Expert, Data Analyst, Synthesizer

## Consulting Frameworks

### 1. Business Diagnostic (Day 1 Framework)
```
Week 1: Discovery
  - Stakeholder interviews (CEO, CFO, COO, key VPs)
  - Financial data analysis (last 3 years P&L, balance sheet)
  - Process mapping (value stream analysis)
  - Competitive positioning assessment
  - Customer satisfaction audit (NPS, CSAT, interviews)

Week 2: Analysis
  - Issue tree (MECE: Mutually Exclusive, Collectively Exhaustive)
  - Root cause analysis (5 Whys, fishbone diagram)
  - Benchmarking against industry best practices
  - Financial modeling (base case + scenarios)

Week 3: Recommendations
  - Hypothesis-driven solution design
  - Prioritization matrix (impact vs. effort)
  - Implementation roadmap (quick wins + strategic initiatives)
  - Business case with ROI projections

Deliverable: 40-60 slide strategy presentation + executive summary
```

### 2. Process Excellence (Lean/Six Sigma)
```
DMAIC Methodology:
  Define:   Problem statement, project charter, SIPOC diagram
  Measure:  Current performance baseline, data collection plan
  Analyze:  Root cause analysis, process capability
  Improve:  Solution design, pilot, validation
  Control:  Control plan, SOPs, monitoring dashboard

Value Stream Mapping:
  → Map all steps from customer order to delivery
  → Identify waste (TIMWOOD): Transportation, Inventory, Motion,
    Waiting, Overprocessing, Overproduction, Defects
  → Design future state with waste eliminated
  → Quantify savings: time saved, cost reduced, quality improved
```

### 3. Digital Transformation Roadmap
```
Maturity Assessment (1-5 scale):
  Digital Strategy:     [1-5] Is digital embedded in business strategy?
  Customer Experience:  [1-5] Digital touchpoints and personalization?
  Operations:           [1-5] Automation and intelligent workflows?
  Technology:           [1-5] Modern stack, cloud, API-first?
  Data & Analytics:     [1-5] Data-driven decisions, AI/ML usage?
  Culture & People:     [1-5] Digital skills, agile ways of working?

Transformation Roadmap:
  Year 1: Foundation (cloud migration, data platform, agile ways of working)
  Year 2: Capability (AI/ML pilots, digital products, process automation)
  Year 3: Scale (AI at scale, new digital revenue streams, ecosystem play)
```

### 4. McKinsey 7S Framework
```
Analyze organizational alignment across:
  Strategy:   Direction and choices for competitive advantage
  Structure:  Organizational hierarchy and reporting
  Systems:    Processes and information flows
  Style:      Leadership approach and culture
  Staff:      People capability and talent
  Skills:     Organizational core competencies
  Shared Values: Guiding principles and culture

All 7 elements must be aligned for transformation to succeed.
```

### 5. Consulting Deliverable Templates
| Deliverable | Format | Pages | Timeline |
|-------------|--------|-------|---------|
| Strategy Presentation | PPTX | 40-60 | 3 weeks |
| Process Improvement Report | PDF | 20-30 | 2 weeks |
| Business Case | XLSX + PDF | 10-15 | 1 week |
| Org Design Report | PPTX | 25-35 | 2 weeks |
| Implementation Roadmap | PPTX | 15-20 | 1 week |
| Executive Summary | PDF | 2-3 | 3 days |

## Revenue Model
- **Subscription**: $450/mo
- **Project Engagement**: $10,000-$100,000+ per project
- **Retainer**: $5,000-$20,000/mo for ongoing advisory
- **Credits**: 20-60 per consulting deliverable

## Example Invocations
- "CONSULT-PRO: Conduct a business diagnostic for our e-commerce operations"
- "Build a digital transformation roadmap for a traditional UAE retail company"
- "CONSULT-PRO: Design a new organizational structure for our 50-person company post-Series A"
