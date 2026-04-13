#!/usr/bin/env python3
"""
DIAW Trading — Prospect Scorer
Calculates BANT + composite scores for sales prospects.
Usage: python prospect-scorer.py --input prospects.json --output scored.json
"""

import json
import argparse
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class BANTScore:
    budget: int      # 0-25
    authority: int   # 0-25
    need: int        # 0-25
    timeline: int    # 0-25

    @property
    def total(self) -> int:
        return self.budget + self.authority + self.need + self.timeline


@dataclass
class ProspectScore:
    company: str
    bant: BANTScore
    fit_score: int          # 0-20 (firmographic match)
    intent_signals: int     # 0-15 (behavioral signals)
    contact_access: int     # 0-15 (decision maker access)
    competitive_position: int  # 0-10 (our position vs alternatives)

    @property
    def composite_score(self) -> float:
        """Composite score: BANT(40%) + Fit(20%) + Intent(15%) + Contact(15%) + Competitive(10%)"""
        return (
            self.bant.total * 0.40 +
            self.fit_score * 0.20 +
            self.intent_signals * 0.15 +
            self.contact_access * 0.15 +
            self.competitive_position * 0.10
        )

    @property
    def grade(self) -> str:
        score = self.composite_score
        if score >= 90: return "A+"
        elif score >= 80: return "A"
        elif score >= 65: return "B"
        elif score >= 50: return "C"
        else: return "D"

    @property
    def action(self) -> str:
        grade = self.grade
        actions = {
            "A+": "Immediate outreach — assign to senior AE, fast-track to demo",
            "A": "Immediate outreach — assign to AE, schedule discovery call",
            "B": "Nurture sequence — educational content, monthly check-in",
            "C": "Low-touch automation — quarterly newsletter, event invites",
            "D": "Disqualify or move to long-term marketing list"
        }
        return actions.get(grade, "Unknown")

    @property
    def recommended_modules(self) -> list:
        """Suggest DIAW modules based on pain points"""
        return []  # Override with actual pain point analysis


def score_prospect(data: dict) -> ProspectScore:
    """Score a prospect from raw data dictionary."""
    bant = BANTScore(
        budget=data.get("budget_score", 0),
        authority=data.get("authority_score", 0),
        need=data.get("need_score", 0),
        timeline=data.get("timeline_score", 0),
    )
    return ProspectScore(
        company=data.get("company", "Unknown"),
        bant=bant,
        fit_score=data.get("fit_score", 0),
        intent_signals=data.get("intent_signals", 0),
        contact_access=data.get("contact_access", 0),
        competitive_position=data.get("competitive_position", 0),
    )


def score_from_file(input_path: str, output_path: str):
    with open(input_path) as f:
        prospects = json.load(f)

    results = []
    for p in prospects:
        scored = score_prospect(p)
        results.append({
            "company": scored.company,
            "composite_score": round(scored.composite_score, 1),
            "grade": scored.grade,
            "action": scored.action,
            "bant": asdict(scored.bant),
            "breakdown": {
                "fit": scored.fit_score,
                "intent": scored.intent_signals,
                "contact": scored.contact_access,
                "competitive": scored.competitive_position,
            }
        })

    # Sort by composite score descending
    results.sort(key=lambda x: x["composite_score"], reverse=True)

    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"Scored {len(results)} prospects. Top 5:")
    for r in results[:5]:
        print(f"  {r['grade']} ({r['composite_score']}) — {r['company']}: {r['action'][:50]}...")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DIAW Prospect Scorer")
    parser.add_argument("--input", required=True, help="Input JSON file with prospect data")
    parser.add_argument("--output", required=True, help="Output JSON file for scored prospects")
    args = parser.parse_args()
    score_from_file(args.input, args.output)
