---
name: diaw-operations
description: >
  DIAW Trading Operations & Scale Engine. Handles SOP creation, process
  automation, hiring playbooks, delegation frameworks, OKR management,
  sprint planning, incident response, business continuity, vendor management,
  organizational design, onboarding workflows, and performance management.
  Activates on SOP, process, automation, workflow, hire, recruit, delegate,
  OKR, sprint, incident, team, onboarding, vendor, org chart.
user-invocable: true
model: claude-opus-4-6
effort: high
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - WebSearch
  - mcp__linear__*
  - mcp__slack__*
---

# DIAW OPERATIONS & SCALE ENGINE v3.0

## 1. SOP BUILDER

### SOP Template
```markdown
# SOP: [Process Name]

| Field | Value |
|-------|-------|
| Owner | [Role/Person] |
| Version | [X.Y.Z] |
| Last Updated | [YYYY-MM-DD] |
| Review Cycle | [Monthly/Quarterly] |
| Frequency | [How often this runs] |
| Est. Duration | [Time to complete] |
| Tools Required | [List] |

## Purpose
[One sentence: why this process exists and what business outcome it drives]

## Trigger
[What initiates this process — event, schedule, or condition]

## Prerequisites
- [ ] [Access/tool/permission needed]
- [ ] [Information/data needed]

## Steps
### Step 1: [Action Verb + Specific Action]
- **Action**: [Detailed instruction]
- **Tool**: [Which tool to use]
- **Output**: [What this step produces]
- **Quality Check**: [How to verify success]
- **Time**: [Expected duration]

## Decision Points
- IF [condition A] → proceed to Step X
- IF [condition B] → escalate to [person/role]

## Exception Handling
| Exception | Action | Escalation |
|-----------|--------|------------|
| [Error type 1] | [Recovery action] | [Contact] |

## Completion Criteria
- [ ] [How to confirm success]
- [ ] [Where to log completion]
- [ ] [Who to notify]

## Metrics
- Success Rate Target: [X%]
- Average Completion Time: [X minutes]
```

### Pre-Built SOPs
| SOP | Flow |
|-----|------|
| Client Onboarding | Trigger → Discovery call → Module selection → Setup → Training → Go-live → 30-day check-in |
| Module Deployment | Request → Architecture review → Agent config → Testing → Staging → Production → Monitoring |
| Incident Response | Alert → Triage (P1-P4) → Investigate → Mitigate → Resolve → Post-mortem → Prevention |
| Content Publishing | Brief → Draft → Edit → SEO → Design → Schedule → Publish → Promote → Measure |
| Sales Qualification | Lead in → Research → Score → Route → (A: outreach, B: nurture, C: automate, D: disqualify) |
| Monthly Reporting | Collect → Dashboard → Analysis → Executive summary → Team review → Action items |
| Hiring | Req approved → JD → Posted → Screen → Phone → Assessment → Interview → Offer → Onboard |

## 2. OKR FRAMEWORK

### Company-Level OKRs (Quarterly)
```
OBJECTIVE 1: Accelerate Revenue Growth
  KR1: Increase MRR from $X to $Y (Z% growth)
  KR2: Acquire N new paying customers
  KR3: Achieve net revenue retention of X%

OBJECTIVE 2: Build World-Class Product
  KR1: Launch X new modules to production
  KR2: Achieve NPS score of X+
  KR3: Reduce average response time to <200ms

OBJECTIVE 3: Build Operational Excellence
  KR1: Achieve 99.9% uptime across all modules
  KR2: Reduce customer onboarding time to <48 hours
  KR3: Maintain employee NPS of X+
```

### OKR Cadence
- Annual OKRs set in December → Reviewed quarterly
- Quarterly OKRs set in first week of quarter → Reviewed monthly
- Weekly key results check-ins every Monday
- Monthly exec review with board update

## 3. HIRING PLAYBOOK

### Hiring Process (7 stages)
1. **Requisition**: Role approved by CEO/CFO, budget allocated, JD written
2. **Sourcing**: LinkedIn, GitHub, referrals, AngelList, job boards
3. **Screen**: Resume review, culture fit check, salary alignment
4. **Phone Screen**: 30-min call — background, motivation, basic qualification
5. **Assessment**: Take-home project (2-3 hours max, paid $100-200)
6. **Team Interview**: 3 interviewers, structured questions, scorecard
7. **Offer**: Written offer within 48h of decision, 3-day response window

### Key Hires (Priority Order)
| Role | When | Salary Range (UAE) |
|------|------|--------------------|
| Head of Engineering | Month 1-3 | AED 25k-40k/mo |
| Sales Lead | Month 2-4 | AED 15k-25k + commission |
| Customer Success | Month 3-6 | AED 12k-20k/mo |
| Marketing Manager | Month 4-6 | AED 12k-18k/mo |
| DevOps Engineer | Month 3-5 | AED 18k-28k/mo |

## 4. AUTOMATION WORKFLOWS

### High-Impact Automations
| Process | Tool | Time Saved | Trigger |
|---------|------|------------|---------|
| Lead scoring | n8n + HubSpot | 3h/day | New lead enters CRM |
| Invoice generation | Stripe + Zapier | 1h/day | Subscription payment |
| Client onboarding | Make + Notion | 4h/client | Contract signed |
| Social media publishing | Buffer + Make | 2h/day | Content calendar |
| Monthly reporting | Python + Sheets | 6h/month | First of month |
| Security scanning | GitHub Actions | 2h/PR | Code push |

## 5. INCIDENT RESPONSE

### Severity Levels
| Level | Criteria | Response Time | Escalation |
|-------|----------|---------------|-----------|
| P1 — Critical | Data loss, full outage, security breach | Immediate | CEO + CTO within 15min |
| P2 — High | Major feature broken, >50% users affected | 30 minutes | Engineering lead + on-call |
| P3 — Medium | Minor feature broken, workaround available | 4 hours | Assigned engineer |
| P4 — Low | Cosmetic issue, minor inconvenience | Next sprint | Ticket queue |

### Post-Mortem Template
```
INCIDENT: [Title] | DATE: [When] | DURATION: [How long] | SEVERITY: [P1-P4]
IMPACT: [Who/what affected, $ impact]

TIMELINE:
  [Time] — [Event]
  [Time] — [Detection]
  [Time] — [Response]
  [Time] — [Resolution]

ROOT CAUSE: [Technical explanation]
CONTRIBUTING FACTORS: [What made this possible / delayed response]
ACTION ITEMS:
  - [ ] [Prevention] — Owner: [Name] — Due: [Date]
  - [ ] [Detection improvement] — Owner: [Name] — Due: [Date]
LESSONS LEARNED: [What we'll do differently]
```
