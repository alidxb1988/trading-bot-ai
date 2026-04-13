---
name: diaw-documents
description: >
  DIAW Trading Document Generation Engine. Creates PDF, DOCX, XLSX, and PPTX
  files. Generates professional proposals, reports, invoices, contracts,
  presentations, financial models, and marketing collateral as downloadable
  files. Activates on PDF, report, document, Word, Excel, PowerPoint,
  presentation, spreadsheet, invoice, contract, proposal document, generate file.
user-invocable: true
model: claude-opus-4-6
effort: high
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# DIAW DOCUMENT GENERATION ENGINE v3.0

## 1. SUPPORTED DOCUMENT TYPES

### PDF Generation (reportlab)
```python
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

DIAW_COLORS = {
    'primary': colors.HexColor('#1a1a2e'),
    'accent': colors.HexColor('#e94560'),
    'light': colors.HexColor('#f5f5f5'),
}
```

### DOCX Generation (python-docx)
```python
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
```

### XLSX Generation (openpyxl)
```python
from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, PieChart
from openpyxl.styles import Font, PatternFill, Alignment, Border
```

### PPTX Generation (python-pptx)
```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
```

## 2. DOCUMENT TEMPLATES

### Proposal (PDF/DOCX)
```
Cover:     DIAW logo | Client name | Date | "Prepared by DIAW Trading"
Page 2:    Executive Summary (problem, solution, ROI, investment)
Page 3:    Situation Analysis (current state, cost of inaction, benchmarks)
Page 4-5:  Recommended Solution (modules, agents, architecture, timeline)
Page 6:    Value Stack & Investment Options (3 tiers)
Page 7:    Implementation Timeline (Gantt chart)
Page 8:    Terms & Next Steps
Appendix:  Technical specs, case studies, team bios
```

### Financial Report (XLSX + PDF)
```
Sheet 1: Dashboard (key metrics with embedded charts)
Sheet 2: Income Statement (monthly columns, annual total)
Sheet 3: Cash Flow Statement
Sheet 4: Balance Sheet
Sheet 5: Unit Economics (CAC, LTV, payback, NRR)
Sheet 6: Revenue by Module (all 20 modules)
Sheet 7: Assumptions & Sensitivity Analysis (data tables)
PDF:     Executive summary with charts exported
```

### Pitch Deck (PPTX — 12 slides)
```
Slide 1:  Cover (logo, tagline, contact)
Slide 2:  Problem (3 bullet points, market data)
Slide 3:  Solution (platform overview)
Slide 4:  Product Demo (screenshot + key features)
Slide 5:  Market Size (TAM/SAM/SOM visual)
Slide 6:  Business Model (revenue streams)
Slide 7:  Traction (MRR chart, customer logos)
Slide 8:  Go-to-Market (channel strategy)
Slide 9:  Competition (positioning matrix)
Slide 10: Team (photos, bios, backgrounds)
Slide 11: Financials (3-year projections chart)
Slide 12: The Ask (amount, use of funds, milestones)
```

### Monthly Client Report (PDF)
```
Page 1: Cover + executive summary (MRR, users, uptime)
Page 2: KPI dashboard (module utilization, agent activity)
Page 3: Module performance breakdown
Page 4: Swarm activity & cost savings vs. unrouted
Page 5: Next month priorities & recommendations
```

### Invoice (PDF)
```
Header:  DIAW Trading logo | Address | TRN (UAE) | Invoice #
Client:  Name, address, account number, billing period
Line Items:
  - Module name | Tier | Monthly fee
  - Credits consumed | Overage rate | Overage total
  - Professional services | Hours | Rate | Total
Subtotal | VAT (5% UAE) | Total Due
Payment: Bank details | Stripe payment link | Due date
Footer:  Terms reference | Support contact
```

## 3. GENERATION SCRIPTS

### Quick Generate Commands
```bash
# Install dependencies
pip install reportlab python-docx openpyxl python-pptx matplotlib

# Generate proposal PDF
python .claude/skills/diaw-documents/scripts/doc-generator.py \
  --type proposal \
  --client "Acme Corp" \
  --modules "OMNI-DROP,GROWTH-ENGINE" \
  --output ./output/acme-proposal.pdf

# Generate financial model XLSX
python .claude/skills/diaw-documents/scripts/doc-generator.py \
  --type financial \
  --year 1 \
  --scenario base \
  --output ./output/year1-model.xlsx

# Generate pitch deck PPTX
python .claude/skills/diaw-documents/scripts/doc-generator.py \
  --type pitch-deck \
  --round "Series A" \
  --ask 5000000 \
  --output ./output/series-a-deck.pptx
```

## 4. BRAND STANDARDS

### DIAW Visual Identity
```
Primary Color:   #1a1a2e (Deep Navy)
Accent Color:    #e94560 (Vibrant Red)
Secondary:       #16213e (Dark Blue)
Text:            #ffffff (White) on dark | #1a1a2e (Navy) on light
Font (headers):  Inter Bold / Montserrat Bold
Font (body):     Inter Regular / Open Sans
Logo placement:  Top-left on all pages, minimum size 40px height
```
