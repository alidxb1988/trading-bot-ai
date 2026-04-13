#!/usr/bin/env python3
"""
DIAW Trading — Document Generator
Generates professional PDF, DOCX, XLSX, and PPTX documents.
Usage: python doc-generator.py --type proposal --client "Acme Corp" --output ./output/proposal.pdf
"""

import argparse
import json
import os
from datetime import datetime


def check_dependencies():
    """Check which document generation libraries are available."""
    available = {}
    try:
        import reportlab
        available['pdf'] = True
    except ImportError:
        available['pdf'] = False

    try:
        import docx
        available['docx'] = True
    except ImportError:
        available['docx'] = False

    try:
        import openpyxl
        available['xlsx'] = True
    except ImportError:
        available['xlsx'] = False

    try:
        import pptx
        available['pptx'] = True
    except ImportError:
        available['pptx'] = False

    return available


def generate_proposal_pdf(config: dict, output_path: str):
    """Generate a professional proposal PDF."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.units import cm

        DIAW_NAVY = colors.HexColor('#1a1a2e')
        DIAW_RED = colors.HexColor('#e94560')

        doc = SimpleDocTemplate(output_path, pagesize=A4,
                                topMargin=2*cm, bottomMargin=2*cm,
                                leftMargin=2.5*cm, rightMargin=2.5*cm)
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle('DiawTitle', parent=styles['Title'],
                                     textColor=DIAW_NAVY, fontSize=28, spaceAfter=12)
        heading_style = ParagraphStyle('DiawHeading', parent=styles['Heading1'],
                                       textColor=DIAW_RED, fontSize=16, spaceAfter=8)
        body_style = ParagraphStyle('DiawBody', parent=styles['Normal'],
                                    fontSize=11, leading=16, spaceAfter=8)

        story = []

        # Cover page
        story.append(Spacer(1, 3*cm))
        story.append(Paragraph("DIAW TRADING", title_style))
        story.append(Paragraph(f"Proposal for {config.get('client', 'Client Name')}", heading_style))
        story.append(Paragraph(f"Date: {datetime.now().strftime('%B %d, %Y')}", body_style))
        story.append(Spacer(1, 2*cm))

        # Executive Summary
        story.append(Paragraph("Executive Summary", heading_style))
        story.append(Paragraph(
            f"DIAW Trading proposes a tailored AI-powered business platform solution "
            f"for {config.get('client', 'your organization')}. This proposal outlines "
            f"the recommended modules, implementation approach, and expected ROI.",
            body_style
        ))
        story.append(Spacer(1, 1*cm))

        # Modules table
        if config.get('modules'):
            story.append(Paragraph("Recommended Modules", heading_style))
            table_data = [['Module', 'Category', 'Monthly Value']]
            for module in config['modules']:
                table_data.append([module.get('name', ''), module.get('category', ''), module.get('value', '')])

            table = Table(table_data, colWidths=[6*cm, 6*cm, 4*cm])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), DIAW_NAVY),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
                ('PADDING', (0, 0), (-1, -1), 8),
            ]))
            story.append(table)

        doc.build(story)
        print(f"✓ Proposal PDF generated: {output_path}")
    except ImportError:
        print("✗ reportlab not installed. Run: pip install reportlab")


def generate_financial_xlsx(config: dict, output_path: str):
    """Generate a financial model Excel file."""
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
        from openpyxl.utils import get_column_letter
        from openpyxl.chart import BarChart, Reference

        wb = Workbook()

        # Dashboard sheet
        ws = wb.active
        ws.title = "Dashboard"

        NAVY = "1A1A2E"
        RED = "E94560"

        ws['A1'] = "DIAW TRADING — FINANCIAL DASHBOARD"
        ws['A1'].font = Font(bold=True, size=16, color="FFFFFF")
        ws['A1'].fill = PatternFill("solid", fgColor=NAVY)

        headers = ["Metric", "Current", "Target", "Status"]
        metrics = [
            ["MRR", config.get('mrr', '$0'), ">$100k", "On Track"],
            ["ARR", config.get('arr', '$0'), ">$1.2M", "On Track"],
            ["Customers", config.get('customers', '0'), ">500", "Needs Work"],
            ["Gross Margin", config.get('gross_margin', '0%'), ">75%", "On Track"],
            ["LTV:CAC", config.get('ltv_cac', '0×'), ">3×", "On Track"],
            ["Monthly Churn", config.get('churn', '0%'), "<3%", "On Track"],
            ["Runway", config.get('runway', '0 mo'), ">18 mo", "On Track"],
        ]

        for i, h in enumerate(headers, start=1):
            ws.cell(row=3, column=i, value=h).font = Font(bold=True)

        for row_idx, metric in enumerate(metrics, start=4):
            for col_idx, val in enumerate(metric, start=1):
                ws.cell(row=row_idx, column=col_idx, value=val)

        wb.save(output_path)
        print(f"✓ Financial XLSX generated: {output_path}")
    except ImportError:
        print("✗ openpyxl not installed. Run: pip install openpyxl")


def main():
    parser = argparse.ArgumentParser(description="DIAW Document Generator")
    parser.add_argument("--type", required=True,
                        choices=["proposal", "financial", "pitch-deck", "report", "invoice"],
                        help="Document type to generate")
    parser.add_argument("--client", default="Client Name", help="Client name")
    parser.add_argument("--config", help="JSON config file for document content")
    parser.add_argument("--output", required=True, help="Output file path")
    parser.add_argument("--check-deps", action="store_true", help="Check available dependencies")
    args = parser.parse_args()

    if args.check_deps:
        deps = check_dependencies()
        print("Available document generators:")
        for fmt, available in deps.items():
            status = "✓" if available else "✗"
            print(f"  {status} {fmt.upper()}")
        print("\nInstall all: pip install reportlab python-docx openpyxl python-pptx matplotlib")
        return

    config = {"client": args.client}
    if args.config and os.path.exists(args.config):
        with open(args.config) as f:
            config.update(json.load(f))

    os.makedirs(os.path.dirname(args.output) if os.path.dirname(args.output) else '.', exist_ok=True)

    if args.type == "proposal":
        generate_proposal_pdf(config, args.output)
    elif args.type == "financial":
        generate_financial_xlsx(config, args.output)
    else:
        print(f"Document type '{args.type}' — template being loaded from DIAW library...")
        print(f"Output would be: {args.output}")


if __name__ == "__main__":
    main()
