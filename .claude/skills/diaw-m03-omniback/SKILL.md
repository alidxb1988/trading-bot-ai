---
name: diaw-m03-omniback
description: >
  OMNIBACK-Ω: AI-powered backend development module. Builds production-ready
  APIs, microservices, database schemas, authentication systems, and cloud
  infrastructure using multi-agent swarms. Handles architecture design, code
  generation, testing, documentation, and deployment pipelines. Activates on
  OMNIBACK, backend, API, microservices, database, authentication, cloud, infrastructure.
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
  - mcp__github__*
---

# OMNIBACK-Ω: Backend Development Module v3.0

## Agent Swarm Configuration
- **Topology**: Hierarchical | **Max Agents**: 6 | **Quality Gate**: 0.98
- **Agents**: Architect Agent, API Agent, Database Agent, Auth Agent, DevOps Agent, QA Agent

## Development Workflow

### Phase 1: Architecture Design (Architect Agent)
- System design document with component diagram
- Technology stack selection (Node.js/Python/Go based on requirements)
- Database selection (PostgreSQL, MongoDB, Redis, Elasticsearch)
- API design (REST vs GraphQL vs gRPC decision)
- Scalability plan (target: 10× current load capacity)

### Phase 2: Core Development
```
API Agent:
  - RESTful endpoints with OpenAPI 3.0 spec
  - Input validation (Joi/Zod/Pydantic)
  - Rate limiting and throttling
  - Response caching strategy

Database Agent:
  - Schema design with normalization
  - Migration scripts (Prisma/Flyway/Alembic)
  - Index optimization for query patterns
  - Seed data for development/testing

Auth Agent:
  - JWT + Refresh token implementation
  - OAuth 2.0 / OIDC integration (Google, GitHub, Apple)
  - RBAC with permission matrices
  - MFA support (TOTP, SMS, email)
```

### Phase 3: Infrastructure (DevOps Agent)
```yaml
# Auto-generated infrastructure
services:
  api:        Docker + Kubernetes
  database:   Managed (RDS/Cloud SQL/Atlas)
  cache:      Redis Cluster
  queue:      Bull/BullMQ or AWS SQS
  storage:    S3/GCS with CDN
  monitoring: Prometheus + Grafana
  logging:    ELK Stack or Datadog
  CI/CD:      GitHub Actions or GitLab CI
```

### Phase 4: Testing (QA Agent)
- Unit tests (Jest/Pytest) — target 80%+ coverage
- Integration tests for all API endpoints
- Load testing (k6) — baseline + 10× load scenarios
- Security testing (OWASP checks)

## Tech Stack Defaults
| Layer | Primary | Alternative |
|-------|---------|-------------|
| Runtime | Node.js (TypeScript) | Python (FastAPI) |
| Database | PostgreSQL + Prisma | MongoDB + Mongoose |
| Cache | Redis | Memcached |
| Queue | BullMQ | AWS SQS |
| Auth | Clerk / Auth0 | Custom JWT |
| Hosting | Railway / Render | AWS ECS / GCP Run |

## Revenue Model
- **Subscription**: $450/mo
- **Setup/Build Fee**: $2,000-$10,000 per project
- **Hourly Support**: $150/hr
- **Credits**: 25-75 per backend build

## Example Invocations
- "OMNIBACK-Ω: Build a multi-tenant SaaS API with Stripe billing and RBAC"
- "Create a real-time trading platform backend with WebSocket support"
- "OMNIBACK-Ω: Generate a complete e-commerce backend with inventory management"
