---
name: diaw-sales
description: >
  DIAW Trading Sales & Prospecting Engine. Handles prospect research, lead
  qualification (BANT+MEDDIC), ICP building, territory planning, competitive
  intelligence, outreach sequences (email + LinkedIn + phone), objection
  handling, proposal drafting, deal tracking, revenue operations, and
  pipeline management. Activates on prospect, lead, qualify, outreach,
  cold email, objection, proposal, deal, pipeline, CRM, ICP, territory.
user-invocable: true
model: claude-opus-4-6
effort: high
context: fork
agent: sales-researcher
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - WebSearch
  - mcp__firecrawl__*
---

# DIAW SALES & PROSPECTING ENGINE v3.0

## 1. IDEAL CUSTOMER PROFILE (ICP) BUILDER

### Firmographic Criteria
- **Industry**: SaaS, fintech, e-commerce, blockchain, professional services
- **Company Size**: 10-500 employees (sweet spot: 50-200)
- **Revenue**: $1M-$100M ARR
- **Funding Stage**: Series A through Series C
- **Geography**: UAE, MENA, Europe, North America
- **Tech Stack Signals**: React, Node, Python, cloud-native, API-first

### Behavioral Signals (High Intent)
- Job postings for AI/ML engineers, DevOps, or platform engineers
- Recent funding round (within 6 months)
- Active on GitHub with growing repositories
- Competitor product mentioned in job descriptions
- Conference attendance or speaking at tech events
- Published blog posts about scaling challenges

### Pain Point Mapping
| Pain Point | DIAW Solution | Module |
|------------|---------------|--------|
| Slow development cycles | Multi-agent swarm development | OMNIBACK-Ω |
| High AI API costs | 3-tier cost routing (75% savings) | Platform Core |
| Security vulnerabilities | Automated security auditing | AEGIS-PRIME |
| Manual business processes | UAE-specific automation | UAE-AUTOMATE |
| Poor e-commerce performance | AI-powered store optimization | OMNI-DROP |
| Crypto portfolio management | AI trading & risk management | ALPHA-OMEGA |
| Scaling marketing | Full-stack growth automation | GROWTH-ENGINE |

## 2. PROSPECT RESEARCH WORKFLOW

### Phase 1: Company Intelligence
```
!firecrawl scrape [company_url] --format markdown --output prospect-intel.md
```
Extract: name, domain, industry, size, funding, revenue estimate, tech stack,
recent news, job postings, social media presence.

### Phase 2: Decision-Maker Mapping
- **Economic Buyer**: CEO, CFO, VP Finance (signs the check)
- **Technical Buyer**: CTO, VP Eng, Head of Platform (evaluates solution)
- **Champion**: Engineering Manager, Team Lead (advocates internally)
- **Coach**: IC engineer, DevRel (provides inside information)
- **Blocker**: Incumbent vendor champion, risk-averse exec (might resist)

### Phase 3: Qualification Scoring

**BANT Score (0-25 each, total 0-100):**
```
Budget:    25=allocated  | 15=needs approval | 5=new allocation needed  | 0=cannot afford
Authority: 25=econ buyer | 15=champion       | 5=influencer only        | 0=no access
Need:      25=urgent     | 15=exploring      | 5=not prioritized        | 0=no need
Timeline:  25=30 days    | 15=90 days        | 5=6 months               | 0=no timeline
```

**MEDDIC Overlay (qualitative):**
- Metrics, Economic Buyer, Decision Criteria, Decision Process, Identify Pain, Champion

**Composite Score:**
```
Score = (BANT × 0.40) + (Fit × 0.20) + (Intent Signals × 0.15) +
        (Contact Access × 0.15) + (Competitive Position × 0.10)
```

**Grades:** A+ (90-100) | A (80-89) | B (65-79) | C (50-64) | D (0-49)
- A+/A → Immediate outreach, fast-track to demo
- B → Nurture sequence, educational content
- C → Low-touch automation, quarterly check-in
- D → Disqualify or long-term marketing list

## 3. COMPETITIVE INTELLIGENCE

### Battle Card Template
```
Competitor: [Name]
├── Strengths: [What they do well]
├── Weaknesses: [Where they fall short]
├── Pricing: [Their pricing model]
├── Key Differentiators vs DIAW:
│   ├── We win on: [specific advantages]
│   ├── They win on: [specific advantages]
│   └── Neutral: [comparable areas]
├── Common Objections When Switching:
│   ├── "[Objection 1]" → Response: "[Counter]"
│   └── "[Objection 2]" → Response: "[Counter]"
├── Migration Path: [How to switch from them to us]
└── Win Rate Against: [X%] based on [data source]
```

## 4. OUTREACH SEQUENCE ENGINE

### Cold Email (7-touch, 21 days)
- **Day 1** — Value-First: Relevant insight, no pitch. CTA: "Curious if you've thought about this?"
- **Day 3** — Case Study: Similar company result with specific numbers.
- **Day 7** — PAS: Problem → Agitate (cost of inaction) → Solution. CTA: "Open to a 15-min walkthrough?"
- **Day 10** — Social Proof: Testimonials, logos, metrics from similar companies.
- **Day 14** — Breakup Warning: "Should I close your file?" + final piece of value.
- **Day 17** — New Angle: Completely different value proposition.
- **Day 21** — Graceful Breakup: Respect time, leave door open.

### LinkedIn (5-touch)
- Touch 1: Connection request + personalized note
- Touch 2: Value message (article/insight)
- Touch 3: Soft pitch ("Helped {similar company} with {result}")
- Touch 4: Direct CTA (demo/consultation/trial)
- Touch 5: Breakup (final offer, leave door open)

### Phone Script
```
Opening (10s):  "Hi {name}, this is [agent] from DIAW. Did I catch you OK? Great — I'll be brief."
Hook (15s):     "I noticed {company} recently {trigger}. We helped {similar} {result}."
Qualify (30s):  "Quick question — how are you handling {pain point}?"
Bridge (15s):   "That's exactly what {module} was built for. {Value prop}."
CTA (10s):      "Would a 20-minute deep dive make sense this week?"
```

## 5. OBJECTION HANDLING PLAYBOOK

| Objection | Type | Response |
|-----------|------|----------|
| "Too expensive" | Price | "ROI math: average client saves ${X}/mo. Pays for itself in {Y} weeks. Plus 75% AI cost reduction." |
| "Using [competitor]" | Competitive | "They're solid at [strength]. Where clients switch: [our differentiator]. Side-by-side?" |
| "Not the right time" | Timing | "What would trigger this becoming a priority? I'll set a reminder." |
| "Need team approval" | Authority | "What questions will your team have? I can prep a one-pager for their concerns." |
| "Send me info" | Stall | "Happy to — is your bigger pain [A] or [B]? That way I send the right thing." |
| "We'll build in-house" | Build vs Buy | "For core IP, absolutely. For {module}: 6 engineers × 4 months = $600k+ vs $997/mo in 2 weeks." |
| "We tried AI before" | Skepticism | "Usually fails because [reason]. Our approach: [differentiator]. Live demo with your data?" |
| "Data security?" | Risk | "SOC2 Type II compliant, encrypted at rest/transit, on-prem for Enterprise. Here's our whitepaper." |

## 6. PROPOSAL STRUCTURE (7 Sections)

1. **Executive Summary** — Problem (quantified), Solution (modules), ROI (3 scenarios), Investment
2. **Situation Analysis** — Current state, cost of inaction, market benchmarks vs their performance
3. **Recommended Solution** — Module selection, agent config, implementation approach, timeline
4. **Value Stack** (Hormozi) — Core + Bonuses, itemized. Total Value: ${sum}. Your Investment: ${price}
5. **Investment Options** — Good / Better / Best tiers
6. **Guarantee** — "If you don't see {result} within {timeframe}, we {refund/extend/credit}."
7. **Next Steps** — Signature → Kickoff (48h) → Discovery → Sprint → Go-live

## 7. REVENUE OPERATIONS (RevOps)

### Pipeline Velocity
```
Pipeline Velocity = (# Opportunities × Win Rate × Avg Deal Size) / Sales Cycle Length
```

### Target Metrics
- Win Rate: >25% | Avg Deal: $5,000-$50,000 | Sales Cycle: <45 days | MQL→SQL: >30%

### Territory Planning
| Territory | Priority | Key Industries | Target Customers/Q |
|-----------|----------|----------------|-------------------|
| UAE/Gulf | P1 | Fintech, E-com, Real Estate | 50-100 |
| MENA Expansion | P2 | SaaS, Professional Services | 30-60 |
| Europe | P3 | Tech Startups, Agencies | 20-40 |
| North America | P4 | Enterprise SaaS | 10-20 |
