---
name: diaw-swarm
description: >
  DIAW Trading RuFlow Swarm Orchestration Engine. Handles multi-agent swarm
  coordination, topology selection (hierarchical, pipeline, mesh, map-reduce,
  consensus, expert-panel, red-team/blue-team, broadcast), agent spawning,
  3-tier cost routing, SONA memory management, swarm monitoring, and
  performance optimization. Activates on swarm, agents, orchestration,
  RuFlow, spawn, multi-agent, topology, coordinator, worker, mesh, pipeline,
  map-reduce, consensus.
user-invocable: true
model: claude-opus-4-6
effort: high
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - mcp__ruflo__*
---

# DIAW SWARM ORCHESTRATION ENGINE v3.0

## 1. SWARM TOPOLOGIES (8 Types)

### 1. Hierarchical (Default)
```
           ┌──────────────┐
           │  COORDINATOR  │
           └──────┬───────┘
        ┌─────────┼─────────┐
   ┌────┴───┐ ┌───┴────┐ ┌──┴─────┐
   │Agent 1 │ │Agent 2 │ │Agent 3 │
   └────────┘ └────────┘ └────────┘
```
Best for: Complex multi-step projects, code generation, architecture design.

### 2. Pipeline (Sequential)
```
  Agent A → Agent B → Agent C → Agent D
```
Best for: Data processing, content creation, code review chains.

### 3. Mesh (Peer-to-Peer)
```
  Agent A ←→ Agent B
     ↕    ╲╱    ↕
  Agent C ←→ Agent D
```
Best for: Brainstorming, creative tasks, open-ended exploration.

### 4. Map-Reduce
```
         MAPPER → Shard 1, Shard 2, Shard 3
                          ↓
                       REDUCER
```
Best for: Research at scale, document processing, data analysis.

### 5. Consensus (Voting)
```
  Agent A (solve) + Agent B (solve) + Agent C (solve) → VOTER (best of 3)
```
Best for: Critical decisions, code review, quality assurance.

### 6. Expert Panel (NEW)
```
  Expert A (Domain) + Expert B (Domain) + Expert C (Domain) → SYNTHESIZER
```
Best for: Strategic decisions, multi-domain analysis, due diligence.

### 7. Red-Team / Blue-Team (NEW)
```
  RED TEAM (attacker) vs BLUE TEAM (defender) → ARBITRATOR (judge + fix)
```
Best for: Security audits, stress testing, quality assurance.

### 8. Broadcast (NEW)
```
  BROADCASTER → Agent 1, Agent 2, Agent 3, ..., Agent N (parallel)
```
Best for: Notifications, monitoring, parallel testing, deployment.

## 2. TOPOLOGY SELECTION GUIDE

| Task Type | Recommended Topology | Reason |
|-----------|---------------------|--------|
| Build a full product feature | Hierarchical | Coordinator manages complex dependencies |
| Process 1000 documents | Map-Reduce | Parallel sharding + aggregation |
| Security audit | Red-Team/Blue-Team | Adversarial testing + defense |
| Strategic decision | Expert Panel | Multi-domain expertise |
| Content pipeline | Pipeline | Sequential transformation |
| Creative brainstorm | Mesh | Free-form collaboration |
| Architecture review | Consensus | Multiple independent assessments |
| Deploy to N environments | Broadcast | One-to-many parallel |

## 3. AGENT ROLE DEFINITIONS

### Universal Agent Preamble
```
You are a specialized agent in the DIAW Trading platform swarm.
Role: {ROLE_NAME}
Module: {MODULE_NAME}
Task: {TASK_DESCRIPTION}
Quality threshold: 0.95
Cost tier: {ASSIGNED_TIER}
Report format: structured JSON with confidence scores
Escalate to coordinator if confidence < 0.80
```

### Core Agent Roles
| Role | Responsibilities | Tier |
|------|-----------------|------|
| Coordinator | Task decomposition, quality gate, result aggregation | Tier 3 |
| Researcher | Web search, data extraction, market intelligence | Tier 2 |
| Analyst | Data analysis, pattern recognition, insights | Tier 2-3 |
| Code Generator | Write, review, test code | Tier 3 |
| Security Reviewer | Vulnerability detection, compliance checks | Tier 3 |
| Content Writer | Copy, documentation, marketing content | Tier 2-3 |
| Validator | QA testing, output verification, error detection | Tier 2 |
| Executor | Run scripts, deploy, execute operations | Tier 1-2 |

## 4. SONA MEMORY SYSTEM

### Memory Architecture
```
SONA (Shared Operational Neural Archive):
  episodic_memory:    Recent task history and outcomes
  semantic_memory:    Domain knowledge and learned patterns
  procedural_memory:  Successful workflows and SOPs
  working_memory:     Current task context and state
```

### Memory Operations
```python
# Store learned pattern
sona.store(key="pattern_name", value={"steps": [], "success_rate": 0.95})

# Retrieve context
context = sona.retrieve(key="client_preferences", client_id="acme_corp")

# Cross-agent sharing
sona.broadcast(message="Task complete", result={}, to="coordinator")
```

## 5. SWARM SPAWN COMMANDS

### RuFlow Integration
```bash
# Spawn hierarchical swarm for module build
npx claude-flow@latest swarm \
  --topology hierarchical \
  --coordinator "DIAW Coordinator" \
  --agents 5 \
  --task "Build OMNI-DROP store for {client}" \
  --module "diaw-m01-omnidrop" \
  --quality-gate 0.95

# Spawn red-team security audit
npx claude-flow@latest swarm \
  --topology red-blue \
  --target "api/endpoints" \
  --red-team-size 3 \
  --blue-team-size 3 \
  --arbitrator "CISO Agent" \
  --output security-report.md
```

## 6. SWARM MONITORING & METRICS

| Metric | Target | Alert Threshold |
|--------|--------|----------------|
| Task completion rate | >95% | <90% |
| Average agent response time | <30s | >60s |
| Coordinator utilization | <80% | >90% |
| Cost per swarm task | <$0.50 | >$1.00 |
| Quality gate pass rate | >90% | <80% |
| Memory retrieval accuracy | >95% | <85% |
