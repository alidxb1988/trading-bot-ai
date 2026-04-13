---
name: diaw-m15-uaeautomate
description: >
  UAE-AUTOMATE: AI-powered UAE business automation module. Handles UAE-specific
  business processes including trade license renewals, visa processing, MOHRE
  compliance, WPS (Wages Protection System), emiratization tracking, VAT filing,
  free zone operations, and Arabic business communication. Activates on
  UAE-AUTOMATE, UAE, Emirates, trade license, visa, MOHRE, WPS, emiratization,
  free zone, Arabic, Gulf business.
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

# UAE-AUTOMATE: UAE Business Automation Module v3.0

## Agent Swarm Configuration
- **Topology**: Pipeline | **Max Agents**: 4 | **Quality Gate**: 0.97
- **Agents**: Compliance Coordinator, Documentation Agent, HR Agent, Finance Agent

## UAE-Specific Automation Workflows

### 1. Trade License Management
```
License Renewal Workflow:
  D-60: Alert → Gather documents checklist
  D-45: Submit renewal application (DED / Free Zone Authority)
  D-30: Follow up on approvals, pay fees
  D-15: Receive renewed license, update all systems
  D-0:  Archive old license, notify relevant parties

Documents Required:
  - Current trade license (attested)
  - Tenancy contract (ejari registered)
  - Shareholders/partners passports and visas
  - MOA (Memorandum of Association)
  - Bank reference letter
  - NOC from relevant authorities (if applicable)
```

### 2. Employee Visa Processing (MOHRE/GDRFA)
```
New Employee Visa:
  Step 1: Entry permit (GDRFA) — processing 3-5 days
  Step 2: Status change (if on visit visa) — 3-5 days
  Step 3: Medical fitness test (DHA-approved centers) — 1 day
  Step 4: Emirates ID biometrics (ICA) — scheduled appointment
  Step 5: Residence visa stamping — 2-3 days
  Step 6: Work permit (MOHRE) — 2-3 days

Documents Tracking:
  - Passport validity check (must be 6+ months)
  - Education certificate attestation status
  - Insurance (mandatory Daman/Aman health coverage)
  - NOL card for transportation
```

### 3. WPS (Wages Protection System)
```python
# Automated WPS payroll processing
def process_wps_payroll(employees, payment_date):
    """
    UAE Ministry of Human Resources WPS compliant payroll
    - Must pay within 10 days of month end (mainland)
    - Free zone: within 15 days
    - Penalties: AED 5,000 per employee per violation
    """
    payroll_data = []
    for emp in employees:
        payroll_data.append({
            'employee_id': emp.wps_id,
            'emirate_id': emp.emirates_id,
            'basic_salary': emp.basic,
            'allowances': emp.allowances,
            'deductions': emp.deductions,
            'net_salary': emp.basic + emp.allowances - emp.deductions,
        })
    return generate_wps_file(payroll_data, payment_date)
```

### 4. Emiratization Compliance (NAFIS)
```
Emiratization Targets (2024+):
  Private sector ≥50 employees: 2% Emirati per year
  Banking sector: 10% Emiratis in new hires

NAFIS Program Automation:
  - Track current Emirati headcount
  - Calculate required hires per quarter
  - Post positions on NAFIS portal automatically
  - Report monthly compliance status
  - Calculate incentive subsidies receivable
```

### 5. Free Zone Operations
| Free Zone | Authority | Specialty |
|-----------|-----------|-----------|
| JAFZA | Jafza | Logistics, manufacturing |
| DMCC | DMCC Authority | Commodities, crypto |
| DAFZA | Dubai Airport | Aviation, logistics |
| DIFC | DIFC Authority | Financial services |
| ADGM | ADGM Authority | Financial services, tech |
| Dubai Internet City | TECOM | Tech companies |
| Dubai Media City | TECOM | Media, marketing |

### 6. Arabic Business Communication
- **Email Templates**: Formal Arabic business correspondence (MSA)
- **Document Translation**: English ↔ Arabic with legal terminology
- **Cultural Calendar**: Ramadan working hours, Eid holidays, National Day
- **Meeting Etiquette**: Gulf business culture reminders and scheduling

## Revenue Model
- **Subscription**: $350/mo
- **One-time Setup**: $1,000-$3,000 for initial automation
- **Monthly Retainer**: $500-$1,500 for ongoing compliance monitoring
- **Credits**: 20-60 per automation workflow

## Example Invocations
- "UAE-AUTOMATE: Set up automated trade license renewal reminders and document checklist"
- "Process WPS payroll for 50 employees and generate the bank transfer file"
- "UAE-AUTOMATE: Track emiratization requirements and suggest hiring plan for Q2"
