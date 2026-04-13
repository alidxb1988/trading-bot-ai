---
name: diaw-finance
description: >
  DIAW Trading Financial Intelligence. Handles financial modeling (3-statement,
  DCF, LBO), unit economics (CAC, LTV, payback), pricing strategy, revenue
  forecasting, burn rate & runway analysis, cap table management, pitch deck
  creation, fundraising strategy, treasury management, and investor relations.
  Activates on financial model, P&L, cash flow, burn rate, runway, pricing,
  unit economics, CAC, LTV, valuation, DCF, cap table, pitch deck, fundraise,
  VC, investor, revenue, budget.
user-invocable: true
model: claude-opus-4-6
effort: high
context: fork
agent: financial-modeler
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - WebSearch
---

# DIAW FINANCIAL INTELLIGENCE v3.0

## 1. FINANCIAL MODELING ENGINE

### Income Statement Structure
```
REVENUE
├── Subscription: Free ($0) | Starter ($97) | Growth ($297) | Enterprise ($997) | Custom ($2,500+)
├── Usage-Based Credits: ${overage_rate} × {credits_consumed}
├── Professional Services: ${hourly_rate} × {hours}
├── Marketplace Commission: ${GMV} × {commission_rate}
├── White-Label Licensing: ${license_fee} × {licensees}
├── Affiliate Revenue (NEW)
├── Training Academy (NEW)
├── Data-as-a-Service (NEW)
└── AI Marketplace (NEW)
= TOTAL REVENUE

COGS
├── AI API (Tier 1: $0 | Tier 2: ~$0.0002/call | Tier 3: $0.003-$0.015/call)
├── Cloud Infrastructure (AWS/GCP)
├── Third-Party APIs, CDN, Support
= GROSS PROFIT (Target: 75-85%)

OPEX
├── Engineering | Sales & Marketing | G&A | R&D
= EBITDA → EBIT → NET INCOME
```

## 2. REVENUE PROJECTIONS BY MODULE (Year 1)

| Module | Customers | ARPU/mo | ARR (Conservative-Aggressive) |
|--------|-----------|---------|-------------------------------|
| OMNI-DROP | 80-150 | $180 | $170k-$324k |
| VOYAGER | 40-80 | $220 | $106k-$211k |
| OMNIBACK-Ω | 30-60 | $450 | $162k-$324k |
| EVENTIUM | 60-100 | $140 | $101k-$168k |
| APP-GENESIS | 25-50 | $380 | $114k-$228k |
| ARCHI-MIND | 20-40 | $350 | $84k-$168k |
| TRADE-FLOW | 35-70 | $250 | $105k-$210k |
| ALPHA-OMEGA | 50-100 | $500 | $300k-$600k |
| CHAIN-FORGE | 15-30 | $600 | $108k-$216k |
| FINOVA | 40-80 | $280 | $134k-$269k |
| VOX-AI | 30-60 | $160 | $58k-$115k |
| PIXEL-CRAFT | 50-100 | $120 | $72k-$144k |
| AEGIS-PRIME | 20-40 | $700 | $168k-$336k |
| GROWTH-ENGINE | 60-120 | $300 | $216k-$432k |
| UAE-AUTOMATE | 40-80 | $350 | $168k-$336k |
| STRATEGIC-CMD | 15-30 | $550 | $99k-$198k |
| VISION-AI | 70-140 | $100 | $84k-$168k |
| CONSULT-PRO | 20-40 | $450 | $108k-$216k |
| CROSS-DOMAIN | 10-20 | $800 | $96k-$192k |
| NEXUS-LINK | 30-60 | $200 | $72k-$144k |
| **TOTAL** | **740-1,450** | **$310 avg** | **$2.7M-$5.4M ARR** |

**Year 2:** 3× growth → $8.1M-$16.2M ARR
**Year 3:** 2.5× growth → $20.3M-$40.5M ARR

## 3. UNIT ECONOMICS DASHBOARD

```python
def calculate_unit_economics(data):
    cac = data['sales_marketing_spend'] / data['new_customers']
    arpu = data['mrr'] / data['customers']
    gross_margin = (data['revenue'] - data['cogs']) / data['revenue']
    lifespan = 1 / data['monthly_churn']
    ltv = arpu * gross_margin * lifespan

    return {
        'CAC': cac,
        'LTV': ltv,
        'LTV_CAC': ltv / cac,          # Target: >3.0
        'Payback_months': cac / (arpu * gross_margin),  # Target: <12
        'Gross_margin_pct': gross_margin * 100,  # Target: >75%
        'Runway_months': data['cash'] / data['burn_rate'],
        'NRR': data['nrr'] * 100,      # Target: >110%
    }
```

### Benchmark Targets
| Metric | Seed | Series A | Series B |
|--------|------|----------|----------|
| LTV:CAC | >3× | >3× | >4× |
| Payback | <18 mo | <12 mo | <9 mo |
| Gross Margin | >60% | >70% | >75% |
| Monthly Churn | <5% | <3% | <2% |
| NRR | >100% | >110% | >120% |
| MRR Growth | >20% | >15% | >10% |

## 4. PRICING STRATEGY

### Value-Based Pricing Tiers
| Tier | Price | Target | Credits | SLA |
|------|-------|--------|---------|-----|
| Free | $0 | Developers, evaluation | 10 credits | Community |
| Starter | $97/mo | Freelancers, solopreneurs | 500 credits | Email 48h |
| Growth | $297/mo | SMBs, agencies | 2,000 credits | Email 24h |
| Enterprise | $997/mo | Scale-ups, enterprises | 10,000 credits | Dedicated 4h |
| Custom | $2,500+/mo | Global enterprises | Unlimited | White-glove 1h |

### Usage-Based Overage
- Credits beyond plan: $0.05-$0.20 per credit depending on tier
- Volume discounts: 10% at 5k credits, 20% at 20k credits, 30% at 100k credits

## 5. FUNDRAISING & PITCH DECK

### Pitch Deck Structure (12 Slides)
1. **Cover** — Logo, tagline, contact, date
2. **Problem** — Market pain with data (3 bullet points max)
3. **Solution** — DIAW platform overview, key differentiators
4. **Product Demo** — Screenshot or 60-second demo video
5. **Market Size** — TAM/SAM/SOM with sources
6. **Business Model** — Revenue streams, pricing tiers
7. **Traction** — MRR, customers, growth rate, key metrics
8. **Go-to-Market** — Channels, ICP, customer acquisition strategy
9. **Competition** — Positioning matrix, key differentiators
10. **Team** — Founders + key hires, relevant experience
11. **Financials** — 3-year projections, key assumptions
12. **The Ask** — Amount, use of funds, milestones to next round

### Fundraising Narrative
- **Seed (~$1M-3M)**: Prove product-market fit, hire first 5 engineers, reach $500k ARR
- **Series A (~$5M-15M)**: Scale GTM, expand to 3+ territories, reach $5M ARR
- **Series B (~$20M-50M)**: International expansion, enterprise motion, reach $20M ARR

## 6. SCENARIO PLANNING

| Scenario | Revenue Y1 | Trigger Conditions |
|----------|------------|-------------------|
| Bear Case | $2.7M ARR | Slow customer acquisition, high churn |
| Base Case | $4.0M ARR | Meets targets, normal growth |
| Bull Case | $5.4M ARR | Viral growth, enterprise deals close early |

**Review monthly.** Activate Bull Case if: MRR >120% of forecast for 2 consecutive months.
