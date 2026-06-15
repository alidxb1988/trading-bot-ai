---
name: diaw-trading-master
description: Master orchestration skill for Diaw Trading Import-Export and Gomale Group operations. Use when user mentions Diaw Trading, Gomale Group, GeoTrading, partnership contracts, supply chain Dubai-Dakar, profit distribution, or any entity-level business operations.
metadata:
  author: Aliou Diaw
  version: 1.0.0
---

# Diaw Trading Master Orchestration

## Entity Registry

- **DIAW TRADING IMPORT-EXPORT** — Senegal (RCCM: SN DKR 2021 A 21531, NINEA: 008663248), Parcelles Assainies U.04 N°147, Guédiawaye, Dakar
- **DIAW TRADING LLC** — Dubai, UAE (est. 2017), Al Aweer Central Fruit & Vegetable Market
- **DIAW TECH** — Dubai, UAE (est. 2017), Web/App Dev, Digital Marketing, ITSM, +971 58 208 9724
- **GOMALE GROUP** — Parent company, RCCM CI-Y0P-2009-B-1068, Yopougon, Abidjan (Mathurin Gue, Gérant)
- **GOMALE GENERAL TRADING LLC (GeoTrading)** — Dubai, Licence 1006885 (valid 23/11/2021–22/11/2026), Capital 300,000 AED, Office 401-140 Barsha 1, Warehouse wh2-11a-sh-441 Dubai Industrial City
- **GOMALE INVEST SARL** — RCCM CI-MAN-2022-B-474, NCC 2243704 L, Capital 1,000,000 FCFA. Ownership: Mathurin Gue 80%, Veh Laurick Anderson 10%, Bamba Massandje 10%

## Contract Framework

Partnership: CONTRAT DE PRESTATION DE SERVICES No _/GMGL/DWT/2026
- Aliou Diaw = Directeur Général des Opérations
- Profit distribution: 30% Prestataire / 30% Mandant / 30% reinvested / 10% charitable (5%+5%)
- Approval threshold: ≤ 50,000 AED autonomous; above requires written consent
- Duration: 2 years, renewable
- Governing law: OHADA Uniform Law + subsidiary Ivorian law + UAE commercial law (Dubai ops)
- Arbitration: CCJA (Abidjan)

## Skill Integration Map

This skill orchestrates all other installed skills:

1. **gohighlevel-crm** → CRM, pipelines, client management, invoicing
2. **claude-trading-skills** → Market intelligence, stock screening
3. **customs-trade-compliance** → HS codes, duty optimization, sanctions
4. **claude-mem-memory** → Persistent context across sessions
5. **remotion-video** → Product videos, social media content
6. **google-stitch-design / claude-design-system** → UI/UX, landing pages, mobile apps
7. **ecommerce-operations** → Stripe, inventory, cart management

## Custom Pipelines (GoHighLevel)

**Dubai → Dakar Supply Chain**
Stages: Sourcing → Quotation → Purchase Order → Shipping → Customs → Delivered → Paid

**B2B Client Acquisition**
Stages: Lead → Qualified → Proposal Sent → Negotiation → Won → Lost

## Key Contacts

- Aliou Diaw: diawtrading@gmail.com, +221 77 719 12 30 / +971 55 903 75 29
- Mathurin Gue: gomaleinvest@gmail.com, +225 05 06 18 93 98

For entity details, see `references/entities.md`.
For contract details, see `references/contracts.md`.
For banking details, see `references/banking.md`.
