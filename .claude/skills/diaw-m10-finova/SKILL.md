---
name: diaw-m10-finova
description: >
  FINOVA: AI-powered financial services module. Handles financial planning,
  investment analysis, loan origination systems, payment gateway integration,
  accounting automation, VAT filing (UAE), financial reporting, and fintech
  product development. Activates on FINOVA, financial services, fintech,
  accounting, VAT, payment gateway, loan, investment analysis, financial reporting.
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
  - mcp__stripe__*
---

# FINOVA: Financial Services Module v3.0

## Agent Swarm Configuration
- **Topology**: Hierarchical | **Max Agents**: 4 | **Quality Gate**: 0.98
- **Agents**: Finance Coordinator, Accounting Agent, Compliance Agent, Analytics Agent

## Core Capabilities

### UAE Financial Compliance
- **VAT Filing**: Quarterly VAT returns via FTA e-Services portal
- **Corporate Tax**: UAE CT at 9% on taxable income >AED 375,000 (from June 2023)
- **Economic Substance**: ESR reporting for UAE entities in relevant activities
- **Anti-Money Laundering**: AML/CFT compliance framework
- **DIFC/ADGM**: Regulated financial services in UAE free zones

### Accounting Automation
```
Chart of Accounts:   Auto-generated per business type and industry
Transaction Coding:  ML-based automatic categorization (95%+ accuracy)
Bank Reconciliation: Daily automated matching with bank feeds
Accounts Payable:    Invoice capture (OCR), approval workflow, payment scheduling
Accounts Receivable: Invoice generation, automated reminders, collection tracking
Payroll:             WPS (UAE Wages Protection System) compliant payroll processing
```

### Financial Reporting Suite
| Report | Frequency | Audience |
|--------|-----------|---------|
| P&L Statement | Monthly | Management |
| Balance Sheet | Monthly | Management + Investors |
| Cash Flow | Weekly | CFO |
| KPI Dashboard | Daily | Executive Team |
| Aged Receivables | Weekly | Finance Team |
| Budget vs Actual | Monthly | Department Heads |
| VAT Return | Quarterly | FTA |
| Audit Pack | Annual | Auditors |

### Payment Gateway Integration
```javascript
// Stripe integration (global)
// PayTabs / Telr / HyperPay (UAE/MENA)
// Network International (UAE acquirer)
// Apple Pay / Google Pay support
// BNPL: Tabby, Tamara (UAE BNPL leaders)

const paymentConfig = {
  providers: ['stripe', 'network_intl'],
  currencies: ['AED', 'USD', 'EUR', 'GBP'],
  methods: ['card', 'apple_pay', 'google_pay', 'bank_transfer'],
  installments: { tabby: true, tamara: true },
};
```

### Loan Origination System
- Credit scoring model (bureau integration: Al Etihad Credit Bureau UAE)
- Application workflow (submission → KYC → credit check → approval → disbursement)
- Loan servicing (repayment schedules, delinquency management)
- Regulatory compliance (CBUAE consumer finance regulations)

### Fintech Product Templates
- **Digital Wallet**: AED multi-currency wallet with P2P transfers
- **Expense Management**: Corporate card + receipt capture + policy enforcement
- **Treasury Dashboard**: Multi-bank visibility, FX hedging, cash forecasting
- **Revenue-Based Financing**: Automated underwriting based on business metrics

## Revenue Model
- **Subscription**: $280/mo
- **Implementation**: $1,000-$5,000 per module setup
- **Transaction Fee**: 0.1-0.5% on payments processed
- **Credits**: 20-60 per fintech product build

## Example Invocations
- "FINOVA: Set up automated VAT filing and accounting for a UAE e-commerce business"
- "Build a digital wallet with AED/USD conversion and payment gateway integration"
- "FINOVA: Create a financial dashboard showing real-time P&L and cash position"
