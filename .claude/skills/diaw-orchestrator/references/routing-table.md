# DIAW Orchestrator — Routing Table v3.0

## Keyword → Skill Mapping

| Keywords | Skill | Priority |
|----------|-------|----------|
| prospect, lead, qualify, BANT, MEDDIC, outreach, cold email, LinkedIn, objection, proposal, deal, pipeline, CRM, ICP, territory | diaw-sales | P1 |
| copy, headline, landing page, SEO, keyword, email campaign, social media, ads, PPC, content, brand, funnel, CRO, A/B test, analytics, AI-SEO | diaw-marketing | P1 |
| financial model, P&L, cash flow, burn rate, runway, pricing, unit economics, CAC, LTV, DCF, cap table, pitch deck, fundraise, VC | diaw-finance | P1 |
| SOP, process, automation, workflow, hire, recruit, delegate, OKR, sprint, incident, team, onboarding, vendor | diaw-operations | P1 |
| market research, TAM, competitor, product-market fit, MVP, validate, roadmap, feature, user research, RICE, ICE | diaw-product | P1 |
| security audit, vulnerability, penetration test, SOC2, ISO27001, GDPR, OWASP, compliance, encryption, threat model | diaw-security | P1 |
| swarm, agents, orchestration, RuFlow, spawn, multi-agent, topology, coordinator, mesh, map-reduce, consensus | diaw-swarm | P1 |
| PDF, report, document, Word, Excel, PowerPoint, presentation, spreadsheet, invoice, contract | diaw-documents | P1 |
| OMNI-DROP, e-commerce, dropshipping, Shopify | diaw-m01-omnidrop | P2 |
| VOYAGER, travel, booking, itinerary | diaw-m02-voyager | P2 |
| OMNIBACK, backend, API, microservices | diaw-m03-omniback | P2 |
| EVENTIUM, event, conference, ticketing | diaw-m04-eventium | P2 |
| APP-GENESIS, mobile app, iOS, Android | diaw-m05-appgenesis | P2 |
| ARCHI-MIND, architecture, system design | diaw-m06-archimind | P2 |
| TRADE-FLOW, trade, logistics, supply chain | diaw-m07-tradeflow | P2 |
| ALPHA-OMEGA, crypto, trading bot, portfolio | diaw-m08-alphaomega | P2 |
| CHAIN-FORGE, blockchain, smart contract, NFT | diaw-m09-chainforge | P2 |
| FINOVA, fintech, accounting, VAT, payment | diaw-m10-finova | P2 |
| VOX-AI, voice, speech, IVR, call center | diaw-m11-voxai | P2 |
| PIXEL-CRAFT, design, brand, UI/UX | diaw-m12-pixelcraft | P2 |
| AEGIS-PRIME, cybersecurity, red team | diaw-m13-aegisprime | P2 |
| GROWTH-ENGINE, growth hacking, funnel | diaw-m14-growthengine | P2 |
| UAE-AUTOMATE, UAE, trade license, WPS | diaw-m15-uaeautomate | P2 |
| STRATEGIC-CMD, strategy, board, M&A | diaw-m16-strategiccmd | P2 |
| VISION-AI, image generation, AI images | diaw-m17-visionai | P2 |
| CONSULT-PRO, consulting, transformation | diaw-m18-consultpro | P2 |
| CROSS-DOMAIN, multi-domain, complex project | diaw-m19-crossdomain | P2 |
| NEXUS-LINK, integration, webhook, pipeline | diaw-m20-nexuslink | P2 |

## Multi-Domain Resolution

When a request spans multiple domains, use the following priority:
1. Most explicit keyword match wins (P1 > P2)
2. For equal priority, choose the primary business action (e.g., "write a pitch deck" → diaw-finance, not diaw-documents)
3. Log secondary skills to be referenced: "Primary: /diaw-finance + Supporting: /diaw-documents"

## Escalation Rules
- If confidence < 0.70 in routing decision → ask user to clarify
- If request spans 3+ domains → route to CROSS-DOMAIN
- If request is not business-related → respond directly without skill activation
