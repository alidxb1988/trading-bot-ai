---
name: diaw-m06-archimind
description: >
  ARCHI-MIND: AI-powered software architecture design module. Creates system
  architecture documents, technical specs, ADRs (Architecture Decision Records),
  scalability plans, microservices designs, data flow diagrams, and cloud
  infrastructure blueprints. Activates on ARCHI-MIND, architecture, system design,
  technical spec, ADR, microservices, scalability, infrastructure blueprint.
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
---

# ARCHI-MIND: Architecture Design Module v3.0

## Agent Swarm Configuration
- **Topology**: Expert Panel | **Max Agents**: 5 | **Quality Gate**: 0.97
- **Agents**: Systems Architect, Security Architect, Data Architect, Cloud Architect, Synthesizer

## Architecture Deliverables

### 1. System Architecture Document
```markdown
# System Architecture: [Project Name]

## 1. Executive Summary
  Problem statement, solution overview, key architectural decisions

## 2. Context & Constraints
  Business requirements, technical constraints, compliance requirements

## 3. Architecture Overview
  High-level component diagram, technology choices rationale

## 4. Component Design
  Each service: responsibilities, interfaces, data owned, dependencies

## 5. Data Architecture
  Entity relationships, data flows, storage strategy, caching

## 6. Security Architecture
  Auth/authz model, encryption, network segmentation, threat model

## 7. Infrastructure & Deployment
  Cloud provider, regions, containers/serverless, CI/CD pipeline

## 8. Scalability & Performance
  Load estimates, scaling strategy, performance targets (P50/P95/P99)

## 9. Observability
  Logging, metrics, tracing, alerting, dashboards

## 10. Architecture Decision Records (ADRs)
  Each major decision: context, options considered, decision, consequences
```

### 2. Architecture Patterns Library
| Pattern | Use Case | When to Apply |
|---------|----------|---------------|
| Microservices | Complex domains, team autonomy | >5 engineers, clear domain boundaries |
| Event-Driven | Async workflows, decoupling | High throughput, loose coupling needed |
| CQRS + Event Sourcing | Audit trails, complex reads | Financial, compliance-heavy systems |
| BFF (Backend for Frontend) | Multiple client types | Web + mobile + API consumers |
| Saga Pattern | Distributed transactions | Multi-service workflows |
| Strangler Fig | Legacy migration | Gradual system replacement |
| Sidecar | Cross-cutting concerns | Service mesh, observability |

### 3. Build vs Buy Decision Framework
```
Score each option (1-5) on:
  - Build complexity × time × cost
  - Vendor lock-in risk
  - Feature fit (current + future)
  - Support and community
  - Security and compliance

Build if: Core competitive advantage, unique requirements, full control needed
Buy if: Commodity functionality, faster time-to-market, strong vendor options
```

### 4. Scalability Planning
```
Capacity Model:
  Current baseline: [X requests/day, Y GB data, Z users]
  Growth projection: [X% MoM for Y months]
  Target capacity: [10× current baseline]
  Scaling triggers: CPU >70% | Memory >80% | P95 latency >200ms

Scaling Strategy:
  Horizontal: Auto-scaling groups, Kubernetes HPA
  Vertical: Right-sizing instances based on load profiles
  Data: Read replicas, sharding, archive strategy
  CDN: Static assets, API response caching, edge compute
```

## Revenue Model
- **Subscription**: $350/mo
- **Architecture Review**: $2,000-$5,000 (one-time)
- **Ongoing Advisory**: $1,500/mo retainer
- **Credits**: 30-80 per architecture engagement

## Example Invocations
- "ARCHI-MIND: Design a multi-tenant SaaS architecture for 10,000 concurrent users"
- "Create an architecture for a real-time trading platform handling 1M events/sec"
- "ARCHI-MIND: Review our existing monolith and propose a microservices migration plan"
