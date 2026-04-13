---
name: diaw-m16-strategiccmd
description: >
  STRATEGIC-CMD: AI-powered business strategy module. Provides C-level strategic
  advisory, OKR frameworks, board presentation preparation, M&A analysis, market
  entry strategies, competitive positioning, scenario planning, and executive
  decision support. Activates on STRATEGIC-CMD, strategy, OKR, board, M&A,
  market entry, competitive positioning, executive decision, scenario planning.
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

# STRATEGIC-CMD: Strategy Module v3.0

## Agent Swarm Configuration
- **Topology**: Expert Panel | **Max Agents**: 4 | **Quality Gate**: 0.97
- **Agents**: CEO Advisor, CFO Advisor, Market Analyst, Strategy Synthesizer

## Strategic Frameworks Library

### 1. Market Entry Strategy
```
Market Entry Framework:
  1. Market Attractiveness Assessment
     - Market size and growth rate (TAM/SAM)
     - Competitive intensity (Porter's 5 Forces)
     - Regulatory environment
     - Cultural and operational fit

  2. Entry Mode Selection
     - Direct (own entity): Full control, higher investment
     - Partnership/JV: Local expertise, shared risk
     - Acquisition: Speed to scale, pay premium
     - Licensing: Asset-light, limited control
     - Franchise: Proven model, operational leverage

  3. Market Entry Sequencing (UAE Focus)
     Phase 1: Dubai (business hub, international exposure)
     Phase 2: Abu Dhabi (government, energy, sovereign wealth)
     Phase 3: GCC expansion (Saudi Arabia priority)
     Phase 4: MENA broader (Egypt, Morocco, Jordan)
```

### 2. Competitive Strategy (Porter's Generic Strategies)
```
Cost Leadership: Lowest cost producer in category
  → Use: 3-tier AI routing, automation, offshore talent

Differentiation: Unique value that commands premium
  → Use: 20 modules, Arabic-first, UAE specialization

Focus (Niche): Target specific segment with superior service
  → Use: UAE enterprise, GCC fintech, MENA e-commerce
```

### 3. M&A Analysis Framework
```
Acquisition Target Evaluation:
  Strategic Fit:    Does target enhance our core capabilities?
  Cultural Fit:     Team compatibility and values alignment?
  Financial Fit:    Price vs. intrinsic value and synergies?
  Integration Risk: How complex is the integration?

Synergy Calculation:
  Revenue Synergies: Cross-sell, new markets, enhanced product
  Cost Synergies:    Duplicate functions, procurement, infrastructure
  Financial Synergies: Tax optimization, capital structure
  
Valuation Methods:
  DCF:         Intrinsic value based on projected cash flows
  Comps:       Trading multiples of comparable companies
  Precedent:   Transaction multiples from similar M&A deals
  LBO:         Max price private equity would pay
```

### 4. Board Presentation Framework
```
Board Pack Structure (Monthly):
  Executive Dashboard:  MRR, growth, burn, runway — 1 page
  Key Decisions:        3-5 decisions requiring board input
  Financial Review:     P&L, cash flow, balance sheet vs budget
  Commercial Update:    Pipeline, new customers, churn, NRR
  Product Roadmap:      Milestones hit, upcoming priorities
  Risks & Mitigations:  Top 5 risks with mitigation status
  CEO Commentary:       Candid assessment of progress vs plan

Board Communication Rules:
  - No surprises (pre-call board members on sensitive items)
  - Data over narrative (charts > text blocks)
  - Ask for specific decisions, not general opinions
  - Follow up within 24h with meeting minutes
```

### 5. SWOT to Strategy Map
```
SWOT → Strategic Initiatives:

SO Strategies: Use strengths to exploit opportunities
  → "We have world-class AI agent tech (S) + UAE enterprise demand (O)
     = Build enterprise sales motion targeting UAE banks and telcos"

ST Strategies: Use strengths to counter threats
  → "Our cost efficiency (S) + new AI startups entering market (T)
     = Aggressive growth pricing to lock in customers before competition scales"

WO Strategies: Overcome weaknesses by exploiting opportunities
  → "Limited brand awareness (W) + growing AI adoption in GCC (O)
     = Invest in thought leadership content and GITEX presence"

WT Strategies: Minimize weaknesses, avoid threats
  → "No enterprise references (W) + enterprise risk aversion (T)
     = Offer risk-free pilots with success-based pricing"
```

## Revenue Model
- **Subscription**: $550/mo
- **Strategy Sprint**: $5,000-$15,000 per engagement
- **Board Advisory Retainer**: $3,000-$10,000/mo
- **Credits**: 25-70 per strategy deliverable

## Example Invocations
- "STRATEGIC-CMD: Develop our UAE market entry strategy for the banking sector"
- "Prepare our Q2 board presentation with key metrics and strategic decisions"
- "STRATEGIC-CMD: Analyze potential acquisition of [company] — strategic fit and valuation"
