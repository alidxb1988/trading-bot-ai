---
name: diaw-m14-growthengine
description: >
  GROWTH-ENGINE: AI-powered marketing automation and growth hacking module.
  Orchestrates full-funnel growth experiments, content marketing at scale,
  paid acquisition, SEO, email automation, conversion optimization, and
  analytics. Runs growth experiments using ICE/RICE scoring. Activates on
  GROWTH-ENGINE, growth hacking, marketing automation, funnel, growth experiments,
  content marketing, paid acquisition, conversion, analytics.
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
  - mcp__analytics__*
---

# GROWTH-ENGINE: Marketing Automation Module v3.0

## Agent Swarm Configuration
- **Topology**: Map-Reduce | **Max Agents**: 5 | **Quality Gate**: 0.93
- **Agents**: Growth Coordinator, Content Agent, Paid Ads Agent, Analytics Agent, CRO Agent

## Growth Experimentation Framework

### ICE Scoring for Growth Experiments
```
Experiment: [Name]
  Impact:     If this works, how big is the effect? [1-10]
  Confidence: How likely is it to work based on data? [1-10]
  Ease:       How easy to implement and test? [1-10]
  ICE Score:  Impact × Confidence × Ease

Minimum score to run: 125 (e.g., 5×5×5)
Fast-track score: 300+ (e.g., 6×7×8)
```

### Growth Experiment Types
| Experiment | Typical Impact | Speed to Results |
|-----------|---------------|-----------------|
| Headline A/B test | 5-30% CVR change | 1-2 weeks |
| CTA button color/text | 2-15% CVR change | 1 week |
| Onboarding flow change | 10-40% activation | 2-3 weeks |
| Pricing page redesign | 15-50% conversion | 3-4 weeks |
| Email subject line test | 10-30% open rate | 3-5 days |
| Referral program launch | 20-100% K-factor | 4-6 weeks |
| SEO content cluster | 30-200% organic traffic | 8-12 weeks |
| Paid channel test | -20% to +50% ROAS | 2-4 weeks |

### Full-Funnel Growth Stack
```
AWARENESS:
  SEO:    Programmatic SEO (100+ pages), content clusters, link building
  Paid:   Google Ads (search + display), LinkedIn Ads, Meta Ads
  Social: LinkedIn (B2B), Twitter/X, YouTube (tutorials)
  PR:     Startup press (TechCrunch MENA, ArabNet, Wamda)

ACQUISITION:
  Lead Magnets: Free tool, template, assessment, report
  Webinars:    Monthly live demos with Q&A
  Trials:      14-day free trial with guided onboarding
  Community:   Discord/Slack community for free users

ACTIVATION:
  Onboarding:  Progressive disclosure, milestone celebrations
  AHA Moment:  Guide to first value delivered in <5 minutes
  Product Tour: Interactive in-app tutorial

RETENTION:
  Email:       Behavioral trigger sequences (usage-based)
  In-app:      Contextual tips and feature discovery
  Check-ins:   Monthly customer success review (Enterprise)
  Community:   Power user program, beta access, co-creation

REVENUE:
  Expansion:   Usage-based triggers for upgrade prompts
  Upsell:      Higher tier features as natural next step
  Cross-sell:  Adjacent modules (e.g., OMNI-DROP → GROWTH-ENGINE)

REFERRAL:
  Program:     Credits for successful referrals (both parties)
  Partners:    Agency partner program (20-30% commission)
  Affiliates:  Content creator + influencer program
```

### Analytics Dashboard
```javascript
// Key growth metrics tracked weekly
const growthMetrics = {
  acquisition: {
    visitors: 'total unique visitors',
    leadCaptureRate: 'leads / visitors',
    trialStartRate: 'trials / leads',
    cpl: 'cost per lead by channel',
  },
  activation: {
    ahaRate: '% reaching AHA moment in 7 days',
    onboardingCompletion: '% completing all onboarding steps',
    d1d7d30Retention: 'day 1/7/30 user retention',
  },
  revenue: {
    mrr: 'monthly recurring revenue',
    mrrGrowth: 'MoM growth %',
    churn: 'monthly churn rate',
    expansion: 'expansion revenue / total MRR',
    nrr: 'net revenue retention',
  },
  referral: {
    kFactor: 'average referrals per customer',
    referralConversion: '% of referrals who convert',
    nps: 'net promoter score',
  }
};
```

## Revenue Model
- **Subscription**: $300/mo
- **Growth Sprint**: $2,000-$5,000 per 4-week sprint
- **Performance Fee**: 10% of incremental revenue from campaigns
- **Credits**: 20-60 per growth campaign

## Example Invocations
- "GROWTH-ENGINE: Run a full audit of our acquisition funnel and prioritize top 10 experiments"
- "Build a referral program that rewards both referrer and referee with platform credits"
- "GROWTH-ENGINE: Set up an automated email sequence triggered by user behavior signals"
