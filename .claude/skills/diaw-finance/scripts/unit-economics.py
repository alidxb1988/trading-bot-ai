#!/usr/bin/env python3
"""
DIAW Trading — Unit Economics Calculator
Calculates key SaaS metrics: CAC, LTV, LTV:CAC, Payback, NRR, Burn Multiple.
Usage: python unit-economics.py --mrr 50000 --customers 120 --churn 0.025
"""

import argparse
from dataclasses import dataclass


@dataclass
class UnitEconomics:
    mrr: float
    customers: int
    monthly_churn_rate: float
    total_sales_marketing_spend: float
    new_customers: int
    cogs_pct: float  # % of revenue that is COGS
    operating_expenses: float  # monthly OpEx excluding COGS
    cash_balance: float
    nrr: float  # Net Revenue Retention as decimal (1.10 = 110%)

    @property
    def arpu(self) -> float:
        return self.mrr / self.customers if self.customers > 0 else 0

    @property
    def gross_margin(self) -> float:
        return 1 - self.cogs_pct

    @property
    def gross_profit(self) -> float:
        return self.mrr * self.gross_margin

    @property
    def cac(self) -> float:
        return self.total_sales_marketing_spend / self.new_customers if self.new_customers > 0 else 0

    @property
    def avg_lifespan_months(self) -> float:
        return 1 / self.monthly_churn_rate if self.monthly_churn_rate > 0 else float('inf')

    @property
    def ltv(self) -> float:
        return self.arpu * self.gross_margin * self.avg_lifespan_months

    @property
    def ltv_cac_ratio(self) -> float:
        return self.ltv / self.cac if self.cac > 0 else float('inf')

    @property
    def payback_months(self) -> float:
        monthly_margin_per_customer = self.arpu * self.gross_margin
        return self.cac / monthly_margin_per_customer if monthly_margin_per_customer > 0 else float('inf')

    @property
    def monthly_burn(self) -> float:
        return self.operating_expenses - self.gross_profit

    @property
    def runway_months(self) -> float:
        return self.cash_balance / self.monthly_burn if self.monthly_burn > 0 else float('inf')

    @property
    def burn_multiple(self) -> float:
        """Burn Multiple = Net Burn / Net New ARR. Target < 1.5"""
        net_new_arr = (self.new_customers - int(self.customers * self.monthly_churn_rate)) * self.arpu * 12
        return abs(self.monthly_burn * 12) / net_new_arr if net_new_arr > 0 else float('inf')

    def benchmark_check(self, stage: str = "seed") -> dict:
        """Check metrics against stage-appropriate benchmarks."""
        benchmarks = {
            "seed":     {"ltv_cac": 3.0, "payback": 18, "gross_margin": 0.60, "churn": 0.05, "nrr": 1.00},
            "series_a": {"ltv_cac": 3.0, "payback": 12, "gross_margin": 0.70, "churn": 0.03, "nrr": 1.10},
            "series_b": {"ltv_cac": 4.0, "payback": 9,  "gross_margin": 0.75, "churn": 0.02, "nrr": 1.20},
        }
        b = benchmarks.get(stage, benchmarks["seed"])
        return {
            "LTV:CAC": {"value": round(self.ltv_cac_ratio, 2), "target": f">{b['ltv_cac']}×", "pass": self.ltv_cac_ratio >= b["ltv_cac"]},
            "Payback (mo)": {"value": round(self.payback_months, 1), "target": f"<{b['payback']} mo", "pass": self.payback_months <= b["payback"]},
            "Gross Margin": {"value": f"{self.gross_margin*100:.1f}%", "target": f">{b['gross_margin']*100:.0f}%", "pass": self.gross_margin >= b["gross_margin"]},
            "Monthly Churn": {"value": f"{self.monthly_churn_rate*100:.1f}%", "target": f"<{b['churn']*100:.0f}%", "pass": self.monthly_churn_rate <= b["churn"]},
            "NRR": {"value": f"{self.nrr*100:.0f}%", "target": f">{b['nrr']*100:.0f}%", "pass": self.nrr >= b["nrr"]},
        }

    def report(self, stage: str = "seed") -> str:
        checks = self.benchmark_check(stage)
        lines = [
            "=" * 60,
            "DIAW TRADING — UNIT ECONOMICS REPORT",
            "=" * 60,
            f"MRR:           ${self.mrr:>12,.2f}",
            f"ARR:           ${self.mrr * 12:>12,.2f}",
            f"Customers:     {self.customers:>12,}",
            f"ARPU:          ${self.arpu:>12,.2f}/mo",
            "",
            "--- Key Metrics ---",
            f"CAC:           ${self.cac:>12,.2f}",
            f"LTV:           ${self.ltv:>12,.2f}",
            f"LTV:CAC:       {self.ltv_cac_ratio:>12.2f}×",
            f"Payback:       {self.payback_months:>12.1f} months",
            f"Gross Margin:  {self.gross_margin*100:>11.1f}%",
            f"Monthly Churn: {self.monthly_churn_rate*100:>11.1f}%",
            f"NRR:           {self.nrr*100:>11.0f}%",
            f"Monthly Burn:  ${self.monthly_burn:>12,.2f}",
            f"Runway:        {self.runway_months:>12.1f} months",
            f"Burn Multiple: {self.burn_multiple:>12.2f}×",
            "",
            f"--- Benchmark Check ({stage.upper()}) ---",
        ]
        for metric, data in checks.items():
            status = "✓" if data["pass"] else "✗"
            lines.append(f"  {status} {metric:<20} {str(data['value']):<10} (target: {data['target']})")

        passed = sum(1 for d in checks.values() if d["pass"])
        lines += ["", f"Score: {passed}/{len(checks)} benchmarks met", "=" * 60]
        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="DIAW Unit Economics Calculator")
    parser.add_argument("--mrr", type=float, required=True, help="Monthly Recurring Revenue ($)")
    parser.add_argument("--customers", type=int, required=True, help="Total paying customers")
    parser.add_argument("--churn", type=float, default=0.025, help="Monthly churn rate (e.g., 0.025 = 2.5%)")
    parser.add_argument("--sm-spend", type=float, default=10000, help="Monthly sales & marketing spend ($)")
    parser.add_argument("--new-customers", type=int, default=20, help="New customers acquired this month")
    parser.add_argument("--cogs-pct", type=float, default=0.22, help="COGS as % of revenue (e.g., 0.22 = 22%)")
    parser.add_argument("--opex", type=float, default=50000, help="Monthly operating expenses ($)")
    parser.add_argument("--cash", type=float, default=500000, help="Current cash balance ($)")
    parser.add_argument("--nrr", type=float, default=1.10, help="Net Revenue Retention (e.g., 1.10 = 110%)")
    parser.add_argument("--stage", default="seed", choices=["seed", "series_a", "series_b"])
    args = parser.parse_args()

    ue = UnitEconomics(
        mrr=args.mrr,
        customers=args.customers,
        monthly_churn_rate=args.churn,
        total_sales_marketing_spend=args.sm_spend,
        new_customers=args.new_customers,
        cogs_pct=args.cogs_pct,
        operating_expenses=args.opex,
        cash_balance=args.cash,
        nrr=args.nrr,
    )
    print(ue.report(stage=args.stage))


if __name__ == "__main__":
    main()
