---
name: diaw-security
description: >
  DIAW Trading Security & Compliance Engine. Handles security audits,
  vulnerability assessment, penetration testing methodology, OWASP Top 10
  compliance, SOC2 Type II preparation, ISO27001 alignment, GDPR compliance,
  access control design, encryption standards, incident response planning,
  security architecture review, and threat modeling. Integrates Trail of Bits
  patterns for professional-grade static analysis. Activates on security,
  vulnerability, penetration test, SOC2, ISO27001, GDPR, OWASP, compliance,
  access control, encryption, incident response, threat model, audit.
user-invocable: true
model: claude-opus-4-6
effort: max
context: fork
agent: security-auditor
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - WebSearch
---

# DIAW SECURITY & COMPLIANCE ENGINE v3.0

## 1. OWASP TOP 10 (2025) CHECKLIST

- [ ] **A01 — Broken Access Control**: Verify RBAC, privilege escalation, CORS policy
- [ ] **A02 — Cryptographic Failures**: TLS config, encryption at rest, key management, hashing
- [ ] **A03 — Injection**: SQL, NoSQL, OS command, LDAP injection testing
- [ ] **A04 — Insecure Design**: Threat modeling, secure design patterns, abuse case testing
- [ ] **A05 — Security Misconfiguration**: Default credentials, unnecessary features, headers
- [ ] **A06 — Vulnerable Components**: Dependency audit, CVE scanning, SBOM
- [ ] **A07 — Auth Failures**: MFA, session management, password policy, credential stuffing
- [ ] **A08 — Data Integrity Failures**: CI/CD pipeline security, dependency verification
- [ ] **A09 — Logging & Monitoring**: Audit logs, alerting, incident detection, log integrity
- [ ] **A10 — SSRF**: Internal network access, cloud metadata access, URL validation

## 2. SECURITY AUDIT FRAMEWORK

### Static Analysis (Trail of Bits Patterns)
```bash
# CodeQL analysis
codeql database create db --language=javascript --source-root=./src
codeql analyze db codeql/javascript-queries --format=sarif --output=results.sarif

# Semgrep rules
semgrep --config=p/javascript --config=p/nodejs --config=p/owasp-top-ten ./src

# Dependency audit
npm audit --audit-level=moderate
pip-audit --requirement requirements.txt

# Generate SBOM
syft . -o cyclonedx-json > sbom.json
```

### Penetration Testing Checklist
```
RECONNAISSANCE:
  [ ] Subdomain enumeration
  [ ] Port scanning (nmap)
  [ ] Service fingerprinting
  [ ] Technology stack identification

AUTHENTICATION TESTING:
  [ ] Brute force protection (lockout after N attempts)
  [ ] Password complexity enforcement
  [ ] MFA bypass attempts
  [ ] Session token entropy and expiry

AUTHORIZATION TESTING:
  [ ] Horizontal privilege escalation (access other users' data)
  [ ] Vertical privilege escalation (elevate own privileges)
  [ ] IDOR (Insecure Direct Object Reference)
  [ ] JWT manipulation

API SECURITY:
  [ ] Rate limiting on all endpoints
  [ ] Input validation and sanitization
  [ ] Response data minimization
  [ ] GraphQL introspection disabled in production

INFRASTRUCTURE:
  [ ] TLS version (min TLS 1.2, prefer 1.3)
  [ ] Security headers (HSTS, CSP, X-Frame-Options)
  [ ] Cloud storage permissions (no public buckets)
  [ ] Container image scanning
```

## 3. SOC2 TYPE II PREPARATION

### Trust Service Criteria Checklist
```
SECURITY (CC series):
  [ ] CC1: Control Environment (policies, org chart, risk assessment)
  [ ] CC2: Communication (security awareness, incident reporting)
  [ ] CC3: Risk Assessment (threat ID, vulnerability management)
  [ ] CC4: Monitoring (continuous monitoring, KPI tracking)
  [ ] CC5: Control Activities (access reviews, change management)
  [ ] CC6: Logical Access (auth, authorization, network security)
  [ ] CC7: System Operations (incident response, backup, recovery)
  [ ] CC8: Change Management (SDLC, testing, deployment controls)
  [ ] CC9: Risk Mitigation (vendor management, business continuity)

AVAILABILITY:
  [ ] SLA monitoring and uptime tracking
  [ ] Disaster recovery procedures tested
  [ ] Capacity planning and load testing

CONFIDENTIALITY:
  [ ] Data classification policy
  [ ] Encryption at rest (AES-256) and in transit (TLS 1.3)
  [ ] Access controls and NDA management

PRIVACY (GDPR alignment):
  [ ] Privacy notice and consent management
  [ ] Data subject rights (access, deletion, portability)
  [ ] Privacy Impact Assessments for new features
  [ ] Data retention and secure disposal policy
```

## 4. THREAT MODELING (STRIDE)

For each system component, evaluate:
| Threat | Question | Mitigation |
|--------|----------|------------|
| **S**poofing | Can an attacker impersonate someone? | Strong auth, MFA, digital signatures |
| **T**ampering | Can data be modified in transit/rest? | Integrity checks, HMAC, TLS |
| **R**epudiation | Can actors deny their actions? | Audit logging, non-repudiation |
| **I**nformation Disclosure | Can sensitive data leak? | Encryption, access controls, DLP |
| **D**enial of Service | Can the system be made unavailable? | Rate limiting, WAF, CDN, DDoS protection |
| **E**levation of Privilege | Can an attacker gain unauthorized access? | Least privilege, RBAC, input validation |

**Risk Score**: Likelihood (1-5) × Impact (1-5) = Risk (1-25)
- **Mitigate**: Score >12
- **Accept**: Score ≤6 with documentation

## 5. SECURITY ARCHITECTURE STANDARDS

### Encryption Requirements
```
At Rest:    AES-256-GCM for sensitive data, AES-128 acceptable for non-sensitive
In Transit: TLS 1.3 (minimum TLS 1.2), HSTS with 1-year max-age
Passwords:  bcrypt (cost factor 12+) or Argon2id
API Keys:   SHA-256 hashed in database, never stored in plaintext
Secrets:    AWS Secrets Manager / HashiCorp Vault / Azure Key Vault
```

### Access Control Model
```
RBAC Roles:
  admin       → Full platform access
  engineer    → Code, infra, no billing/user management
  analyst     → Read-only data access
  support     → Customer data, no code/infra
  customer    → Own data and modules only

Principles:
  - Least privilege (minimum access required)
  - Separation of duties (no single point of compromise)
  - Zero trust (verify every request, assume breach)
  - Just-in-time access (temporary elevated privileges)
```

## 6. COMPLIANCE AUTOMATION

### Automated Compliance Checks (CI/CD Integration)
```yaml
# .github/workflows/security.yml
security-scan:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v3
    - name: SAST (Semgrep)
      run: semgrep --config=auto --error --json > semgrep-results.json
    - name: Dependency Audit
      run: npm audit --audit-level=high
    - name: Container Scan
      uses: aquasecurity/trivy-action@master
    - name: Secrets Detection
      uses: trufflesecurity/trufflehog@main
    - name: SBOM Generation
      run: syft . -o cyclonedx-json > sbom.json
```
