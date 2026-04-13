---
name: diaw-marketing
description: >
  DIAW Trading Marketing & Growth Engine. Handles copywriting (PAS, AIDA, BAB,
  4Ps, FAB), SEO content, AI-SEO (AEO/GEO/LLMO), programmatic SEO, email
  campaigns, social media strategy, paid advertising, CRO, A/B testing,
  analytics tracking, content marketing, brand strategy, and growth hacking.
  Activates on copy, headline, landing page, SEO, keyword, email campaign,
  social media, ads, PPC, content, brand, funnel, conversion, A/B test,
  CRO, analytics, AI-SEO, growth.
user-invocable: true
model: claude-opus-4-6
effort: high
context: fork
agent: content-strategist
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - WebSearch
  - mcp__firecrawl__*
  - mcp__analytics__*
---

# DIAW MARKETING & GROWTH ENGINE v3.0

## 1. COPYWRITING SYSTEM

### Framework Selection Matrix
| Content Type | Framework | Structure |
|-------------|-----------|-----------|
| Landing pages | AIDA | Attention → Interest → Desire → Action |
| Sales pages | PAS | Problem → Agitate → Solution |
| Email campaigns | BAB | Before → After → Bridge |
| Advertisements | 4Ps | Promise → Picture → Proof → Push |
| Product descriptions | FAB | Features → Advantages → Benefits |
| Case studies | STAR | Situation → Task → Action → Result |
| Testimonial pages | SSS | Struggle → Solution → Success |

### Universal Copy Rules
- Write at 6th-grade reading level (Flesch-Kincaid 60+)
- Lead with benefits, never features
- Use specific numbers ("save 73% on API costs" not "save money")
- Every piece ends with a clear, specific CTA
- Produce 3 variants: Direct, Story-driven, Contrarian
- **Banned phrases**: "In today's fast-paced world", "It goes without saying", "Cutting-edge", "Revolutionary", "Game-changing", "Leverage", "Synergy", "Best-in-class"
- Short sentences. Short paragraphs. White space.

### 20 Headline Formulas
1. How to [Desired Outcome] Without [Pain Point]
2. [Number] Ways to [Benefit] in [Timeframe]
3. The [Adjective] Guide to [Topic] for [Audience]
4. Why [Common Belief] Is Wrong (And What to Do Instead)
5. [Name], Here's How [Similar Company] [Achieved Result]
6. Stop [Bad Action]. Start [Good Action]. Here's How.
7. What [Respected Group] Know About [Topic] That You Don't
8. The [Number]-Step System for [Desired Outcome]
9. [Shocking Statistic] — Here's What It Means for [Audience]
10. Warning: Don't [Action] Until You Read This
11. The Secret to [Outcome] That [Authority] Won't Tell You
12. [Desired Outcome] in [Timeframe] — Guaranteed
13. If You [Situation], You Need to Know About [Solution]
14. [Number] Mistakes [Audience] Make With [Topic]
15. The Last [Product Category] You'll Ever Need
16. Everything You Know About [Topic] Is Wrong
17. How [Company] Went From [Bad State] to [Good State] in [Time]
18. [Number] Proven Strategies for [Outcome] in [Year]
19. What Happens When [Audience] Discovers [Solution]
20. The [Year] Playbook for [Outcome] — [Number] Proven Strategies

## 2. SEO CONTENT ENGINE

### Standard SEO Workflow
1. **Keyword Research**: Primary (1), Secondary (5-10), LSI (10-20), Question (5)
2. **Intent Classification**: Informational / Navigational / Transactional / Commercial
3. **Content Brief**: Title (60 chars), Meta (155 chars), H2 structure, word count, schema
4. **E-E-A-T**: Experience (examples), Expertise (data), Authority (sources), Trust (dates)

```bash
# Firecrawl competitor research
!firecrawl search "[primary keyword]" --limit 10 --output serp-analysis.md
!firecrawl scrape [competitor_url] --format markdown
```

### AI-SEO (NEW in v3.0)

**AEO (Answer Engine Optimization)**
- Structure content to be directly quotable by AI assistants
- Use concise, definitive statements in the first paragraph
- Include FAQ sections with clear Q&A pairs
- Use FAQ schema and HowTo schema

**GEO (Generative Engine Optimization)**
- Use statistics and specific numbers that AI systems prefer to cite
- Create authoritative, well-structured content that LLMs rank highly
- Include unique data, original research, or proprietary insights

**LLMO (Large Language Model Optimization)**
- Create canonical reference content for each service module
- Build topical authority through comprehensive content clusters
- Monitor AI assistant mentions via regular brand audits

## 3. EMAIL CAMPAIGN ARCHITECTURE

### Sequence Types
| Sequence | Emails | Duration | Purpose |
|----------|--------|----------|---------|
| Welcome | 5 | 7 days | Onboard, deliver lead magnet, soft pitch |
| Nurture | 12 | 30 days | Educate, case studies, soft pitches |
| Launch | 7 | 5 days | Announce, benefits, FAQ, testimonials, urgency, close |
| Re-engagement | 3 | 7 days | Win back inactive subscribers |
| Churn Prevention | 3 | 3 days | Save cancelling customers |

### Subject Line Formulas
- `[Name], quick question about [topic]`
- `How to [outcome] without [pain point]`
- `[Number] ways to [benefit]`
- `Did you see this? [curiosity hook]`
- `Re: [topic they engaged with]`
- `[Company] + [DIAW module] = [result]`

### Email Metrics Targets
- Open Rate: >25% | Click Rate: >3% | Reply Rate: >1% | Unsubscribe: <0.5%

## 4. SOCIAL MEDIA STRATEGY

### Platform Playbooks
**LinkedIn (B2B Primary)** — 4-5x/week
- 40% Thought leadership | 25% Case studies | 20% Behind-scenes | 15% CTA
- Post formats by reach: Text stories > Carousels > Polls > Video > Articles

**Twitter/X (Tech Community)** — 2-3x/day
- 35% Tech insights | 25% Product updates | 20% Community | 20% Personality
- Thread format: Hook tweet → 5-10 supporting → CTA/summary

**Instagram (Visual Brand)** — 5-7x/week
- Reels (3-4/wk), Stories (daily), Posts (2-3/wk)
- 3-5 hashtags: Branded + Industry + Niche

**YouTube (Authority Builder)** — 1-2x/week
- Platform demos (10-15 min), Case studies (15-20 min), Tutorials (20-30 min)

## 5. PAID ADVERTISING ENGINE

### Budget Allocation
**Testing Phase (Month 1-2):** $3,000-5,000
- 60% audience testing | 30% creative testing | 10% retargeting

**Scaling Phase (Month 3+):** $5,000-20,000+
- 50% proven winners | 25% lookalike | 15% retargeting | 10% new testing

**Target Metrics:** CPM <$15 | CPC <$3 | CPA <$150 | ROAS >3×

### Retargeting Ladder
1. Cart/checkout abandoners → direct offer + urgency
2. Pricing page visitors → case study + social proof
3. Feature page visitors → relevant demo video
4. Blog readers → lead magnet or free tool
5. Homepage bouncers → brand awareness + value prop

## 6. CONVERSION RATE OPTIMIZATION (CRO)

### Audit Checklist
- [ ] Value prop clear within 3 seconds?
- [ ] Trust signals visible (logos, testimonials, badges)?
- [ ] CTA above fold + after value sections + bottom?
- [ ] Button text action-oriented ("Start Free Trial" not "Submit")?
- [ ] Form fields minimized (name + email for top-of-funnel)?
- [ ] Page speed <2s on mobile?
- [ ] Headline matches traffic source?
- [ ] Objections addressed proactively?

### A/B Testing Framework
1. **Hypothesis**: "Changing [X] to [Y] will improve [metric] by [Z]% because [reason]"
2. **Sample size**: Calculate with 95% confidence, 80% statistical power
3. **Run time**: Minimum 2 weeks, minimum 100 conversions per variant
4. **Analyze**: Check for significance before declaring winner
5. **Iterate**: Winner becomes control, run next test
