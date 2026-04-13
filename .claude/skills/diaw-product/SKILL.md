---
name: diaw-product
description: >
  DIAW Trading Product & Strategy Engine. Handles market research, TAM/SAM/SOM
  analysis, competitive analysis, product-market fit assessment, MVP validation,
  feature prioritization (RICE/ICE), roadmap planning, user research,
  Jobs-to-be-Done analysis, positioning strategy, and product launches.
  Activates on market research, TAM, competitor, product-market fit, MVP,
  validate, roadmap, feature, user research, positioning, RICE, ICE.
user-invocable: true
model: claude-opus-4-6
effort: high
context: fork
agent: market-analyst
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - WebSearch
  - mcp__firecrawl__*
---

# DIAW PRODUCT & STRATEGY ENGINE v3.0

## 1. MARKET RESEARCH FRAMEWORK

### TAM/SAM/SOM Analysis
```
TAM (Total Addressable Market):
  = [# potential customers globally] × [annual value per customer]
  Sources: Gartner, IDC, Statista, public filings

SAM (Serviceable Available Market):
  = TAM × [addressable % based on geography, size, tech requirements]

SOM (Serviceable Obtainable Market):
  = SAM × [realistic market share % over 3-5 years]
```

### DIAW Market Sizing
| Market | TAM | SAM | SOM (3yr) | CAGR |
|--------|-----|-----|-----------|------|
| AI Business Automation | $500B+ | $50B | $500M | 35% |
| UAE Digital Business | $25B | $8B | $80M | 28% |
| Multi-Agent Platforms | $15B | $5B | $50M | 45% |
| E-commerce Automation | $200B | $20B | $200M | 22% |

### Jobs-to-be-Done Framework
```
JOB: When [situation], I want to [motivation], so I can [expected outcome].

Functional: "When I need to build an e-commerce store, I want to automate the
             process, so I can launch in days instead of months."

Emotional: "When I'm scaling my business, I want to feel confident about
            security, so I can focus on growth without worry."

Social: "When I present to investors, I want professional-grade materials,
         so I can appear credible and well-prepared."
```

## 2. COMPETITIVE ANALYSIS

### Feature Comparison Matrix
| Feature | DIAW | Competitor A | Competitor B | Competitor C |
|---------|------|-------------|-------------|-------------|
| Multi-agent swarms | ✓ | ✗ | Partial | ✗ |
| 3-tier cost routing | ✓ | ✗ | ✗ | ✗ |
| 20 unified modules | ✓ | 3-5 | 1-2 | 8-10 |
| MCP + A2A + ACP | ✓ | MCP only | ✗ | Custom |
| Arabic/UAE support | ✓ | ✗ | ✗ | Partial |
| Self-learning agents | ✓ | ✗ | Basic | ✗ |

### Competitive Intelligence Workflow
```bash
!firecrawl search "[competitor name] pricing features 2026" --limit 5
!firecrawl scrape [competitor_url]/pricing --format markdown
```

## 3. PRODUCT-MARKET FIT ASSESSMENT

### Sean Ellis Test
**Survey**: "How would you feel if you could no longer use DIAW Trading?"
- A) Very disappointed → **Target: >40% for confirmed PMF**
- B) Somewhat disappointed
- C) Not disappointed
- D) N/A

### Additional PMF Signals
- Organic growth: >30% of new users from word-of-mouth
- NPS: >50
- Daily active usage: >40% of paying customers
- Retention curve: Flattens (doesn't go to zero)

### PMF Progression Stages
| Stage | Name | Validation Criteria |
|-------|------|---------------------|
| 1 | Problem-Solution Fit | 20+ interviews confirm pain point |
| 2 | Product-Market Fit | >40% "very disappointed" + growing revenue |
| 3 | Channel-Product Fit | LTV:CAC >3× via 2+ channels |
| 4 | Model-Market Fit | Unit economics work at 10× current scale |

## 4. FEATURE PRIORITIZATION

### RICE Scoring
```
RICE Score = (Reach × Impact × Confidence) / Effort

Reach:      # customers affected per quarter [number]
Impact:     Effect on experience [0.25 | 0.5 | 1 | 2 | 3]
Confidence: Certainty of estimates [10%-100%]
Effort:     Person-weeks to implement [number]
```

### ICE Scoring (quick experiments)
```
ICE Score = Impact × Confidence × Ease  [each 1-10]
```

### Roadmap Template
```
NOW (This Sprint):     [2-3 features, highest RICE scores]
NEXT (Next Sprint):    [3-5 features, second tier]
LATER (This Quarter):  [5-10 features, loosely ordered]
FUTURE (Next Quarter): [10+ ideas, not yet prioritized]
ICEBOX:                [Ideas captured, not committed]
```

## 5. MVP VALIDATION PROCESS

### Validation Framework
1. **Hypothesis**: "[Segment] has [problem] and will pay [price] for [solution]"
2. **Test Design**: Smallest experiment to validate/invalidate
3. **Success Criteria**: Define metrics before starting
4. **Build**: Minimum viable version testing core value
5. **Measure**: Track defined metrics over defined timeframe
6. **Learn**: Pivot, persevere, or kill based on data

### MVP Sprint Plan (2 weeks)
- **Day 1-2**: Define hypothesis and success criteria
- **Day 3-5**: Build core feature only (no nice-to-haves)
- **Day 6-8**: Internal testing and bug fixes
- **Day 9-10**: Beta with 10-20 target customers
- **Day 11-12**: Collect feedback and data
- **Day 13-14**: Decision: pivot/persevere/kill

## 6. POSITIONING STRATEGY

### Positioning Statement
```
For [target customer] who [has problem/need],
DIAW Trading is the [category] that [primary differentiation],
unlike [alternatives] which [key limitation].
We [proof point].
```

### Messaging Hierarchy
1. **Primary Message** (tagline): "The AI-Powered Business Operating System"
2. **Value Prop** (1 sentence): What we do + who for + key benefit
3. **Elevator Pitch** (30 sec): Problem → Solution → Proof → CTA
4. **Full Story** (2 min): Full narrative with social proof

### Positioning by Segment
| Segment | Key Message | Proof Point |
|---------|-------------|-------------|
| Tech Startups | "Ship 5× faster with agent swarms" | OMNIBACK-Ω case study |
| E-commerce | "Launch your store in 48 hours" | OMNI-DROP results |
| Enterprises | "Cut AI costs 75% with 3-tier routing" | Cost analysis |
| UAE Businesses | "Built for the UAE market, Arabic-first" | UAE-AUTOMATE module |
