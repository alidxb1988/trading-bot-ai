---
name: diaw-m13-aegisprime
description: >
  AEGIS-PRIME: AI-powered cybersecurity module. Conducts automated security
  audits, penetration testing, vulnerability assessments, compliance checks
  (SOC2, ISO27001, GDPR), security architecture reviews, and incident response.
  Uses Red-Team/Blue-Team swarm topology for adversarial testing. Activates on
  AEGIS-PRIME, cybersecurity, security audit, penetration test, vulnerability,
  compliance, OWASP, red team, blue team, SOC2.
user-invocable: true
context: fork
effort: max
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - WebSearch
  - mcp__ruflo__*
---

# AEGIS-PRIME: Security Module v3.0

## Agent Swarm Configuration
- **Topology**: Red-Team/Blue-Team | **Max Agents**: 5 | **Quality Gate**: 0.99
- **Agents**: Red Team Lead, Red Team Attacker, Blue Team Defender, Security Architect, Report Agent

## Security Assessment Workflow

### Phase 1: Reconnaissance (Red Team)
```bash
# Subdomain enumeration
subfinder -d target.com | httpx -silent | tee subdomains.txt

# Port and service scanning
nmap -sV -sC -T4 --script=default target.com -oA nmap-results

# Technology fingerprinting
whatweb target.com
wappalyzer-cli target.com

# Certificate transparency
crt.sh lookup for target.com
```

### Phase 2: Vulnerability Assessment
```bash
# Web application scanning
nuclei -t ~/nuclei-templates/ -u https://target.com -o nuclei-results.txt

# API security testing
- Test all endpoints in Swagger/OpenAPI spec
- Check for BOLA, BFLA, mass assignment, rate limiting
- Test authentication bypass techniques

# Static code analysis
semgrep --config=p/owasp-top-ten --config=p/javascript ./src

# Dependency vulnerability check
npm audit --audit-level=moderate
trivy fs --severity HIGH,CRITICAL .
```

### Phase 3: Active Exploitation (Controlled)
```
[All testing performed only on authorized systems with explicit written permission]

Authentication:
  - Brute force protection testing
  - Password reset flow analysis
  - MFA bypass testing (backup codes, SIM swap)
  - JWT algorithm confusion attacks

Injection:
  - SQL injection (manual + sqlmap)
  - NoSQL injection (MongoDB operator injection)
  - SSRF (Server-Side Request Forgery)
  - XXE (XML External Entity)

Business Logic:
  - Price manipulation testing
  - Workflow bypass (skip payment step)
  - Privilege escalation (IDOR)
  - Race condition testing
```

### Phase 4: Blue Team Response
```
For each vulnerability found by Red Team:
  1. Classify: Critical / High / Medium / Low / Info
  2. Reproduce: Confirm finding with PoC
  3. Root cause: Identify underlying code/config issue
  4. Remediation: Specific fix recommendation
  5. Verify: Re-test after fix applied
  6. Document: Add to security runbook
```

### Deliverables
```
Security Assessment Report:
  Executive Summary:       Risk posture, critical findings, immediate actions
  Methodology:             Scope, tools, approach, testing timeline
  Findings by Severity:    Critical → High → Medium → Low → Info
  Finding Format:
    Title | Severity | CVSS Score | Description | Evidence | Impact | Remediation
  Remediation Roadmap:     Prioritized fix schedule (immediate/30/60/90 days)
  Compliance Gap Analysis: SOC2 / ISO27001 / GDPR gaps identified
  Appendix:                Tool outputs, screenshots, PoC code
```

## Revenue Model
- **Subscription**: $700/mo
- **One-time Audit**: $3,000-$15,000
- **Ongoing Monitoring**: $1,500/mo retainer
- **Credits**: 25-75 per security engagement

## Example Invocations
- "AEGIS-PRIME: Conduct a full security audit of our API endpoints and authentication system"
- "Run a red-team assessment against our web application for OWASP Top 10 vulnerabilities"
- "AEGIS-PRIME: Prepare our SOC2 Type II compliance documentation and gap analysis"
