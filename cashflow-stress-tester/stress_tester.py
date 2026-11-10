"""
Student Cashflow Stress-Tester
Monte Carlo simulation of a UK student's month-by-month cash balance (Sep -> Jun).

Question it answers: "Given my plan, what is the probability I run out of money,
when is it most likely to happen, and how big a buffer do I need?"

Key modelling choices (see README for limitations):
- Rent runs Sep-Apr (8 payments); bills run Sep-May (9 payments); other spend 10 months.
- Student finance lands in three lumps (Sep / Jan / Apr), with a chance of delay.
- Part-time earnings vary month to month (shift availability, illness, exams).
- Living and "life" spending are noisy; unexpected costs arrive randomly (Poisson).
"""
from dataclasses import dataclass, field
import numpy as np

MONTHS = ["Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun"]


@dataclass
class Plan:
    opening_savings: float = 350.0
    # Money in
    finance_lumps: dict = field(default_factory=lambda: {0: 1600.0, 4: 1600.0, 7: 1600.0})
    family_support_monthly: float = 75.0
    hourly_rate: float = 11.5
    hours_per_week: float = 10.0
    weeks_per_month: float = 3.9
    exam_months: tuple = (8, 9)          # May, Jun: earnings reduced
    exam_earnings_factor: float = 0.4
    # Money out (Tier A locked / B living / C life)
    rent: float = 470.0
    rent_months: range = range(0, 8)     # Sep-Apr
    bills: float = 62.0
    bills_months: range = range(0, 9)    # Sep-May
    living: float = 225.0
    life: float = 125.0
    # Uncertainty parameters
    finance_delay_prob: float = 0.12     # chance a lump arrives one month late
    earnings_sd: float = 0.25            # relative sd of monthly earnings
    spend_sd: float = 0.15               # relative sd of living/life spend
    shock_rate_per_month: float = 0.15   # expected unexpected costs per month
    shock_mean: float = 120.0            # mean size of an unexpected cost


def simulate(plan: Plan, n_sims: int = 20000, seed: int = 42) -> np.ndarray:
    """Return balances array of shape (n_sims, n_months) = end-of-month balance."""
    rng = np.random.default_rng(seed)
    n = len(MONTHS)
    bal = np.full(n_sims, plan.opening_savings, dtype=float)
    out = np.zeros((n_sims, n))
    delayed = np.zeros((n_sims, n))  # carry delayed lumps forward

    for m in range(n):
        inflow = np.full(n_sims, plan.family_support_monthly, dtype=float)

        # Student finance, with chance of one-month delay
        lump = plan.finance_lumps.get(m, 0.0)
        if lump:
            late = rng.random(n_sims) < plan.finance_delay_prob
            inflow += np.where(late, 0.0, lump)
            if m + 1 < n:
                delayed[:, m + 1] += np.where(late, lump, 0.0)
        inflow += delayed[:, m]

        # Earnings: lognormal-ish noise, reduced in exam months
        base = plan.hourly_rate * plan.hours_per_week * plan.weeks_per_month
        if m in plan.exam_months:
            base *= plan.exam_earnings_factor
        inflow += base * np.clip(rng.normal(1.0, plan.earnings_sd, n_sims), 0, None)

        # Outflows
        outflow = np.zeros(n_sims)
        if m in plan.rent_months:
            outflow += plan.rent
        if m in plan.bills_months:
            outflow += plan.bills
        outflow += plan.living * np.clip(rng.normal(1.0, plan.spend_sd, n_sims), 0, None)
        outflow += plan.life * np.clip(rng.normal(1.0, plan.spend_sd, n_sims), 0, None)

        # Random unexpected costs
        k = rng.poisson(plan.shock_rate_per_month, n_sims)
        outflow += k * rng.exponential(plan.shock_mean, n_sims)

        bal = bal + inflow - outflow
        out[:, m] = bal
    return out


def summarise(balances: np.ndarray) -> dict:
    below = balances < 0
    ever = below.any(axis=1)
    return {
        "p_ever_overdrawn": float(ever.mean()),
        "p_overdrawn_by_month": {m: float(below[:, i].mean()) for i, m in enumerate(MONTHS)},
        "median_balance": {m: float(np.median(balances[:, i])) for i, m in enumerate(MONTHS)},
        "p10_balance": {m: float(np.percentile(balances[:, i], 10)) for i, m in enumerate(MONTHS)},
        "worst_month": MONTHS[int(below.mean(axis=0).argmax())],
        # Buffer needed so that only 5% of simulations ever go below zero
        "buffer_for_95pct_safety": float(max(0.0, -np.percentile(balances.min(axis=1), 5))),
    }


def hours_for_safety(plan: Plan, target_p: float = 0.05, n_sims: int = 8000) -> float:
    """Smallest weekly hours (0.5 step) so P(ever overdrawn) <= target_p."""
    import copy
    h = 0.0
    while h <= 40:
        p = copy.deepcopy(plan)
        p.hours_per_week = h
        if summarise(simulate(p, n_sims))["p_ever_overdrawn"] <= target_p:
            return h
        h += 0.5
    return float("nan")


def plot(balances: np.ndarray, path: str = "stress_test.png") -> None:
    """Fan chart: median and percentile bands of the balance, with the zero line."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    x = np.arange(len(MONTHS))
    pct = {q: np.percentile(balances, q, axis=0) for q in (5, 25, 50, 75, 95)}
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.fill_between(x, pct[5], pct[95], alpha=0.15, label="5th-95th percentile")
    ax.fill_between(x, pct[25], pct[75], alpha=0.30, label="25th-75th percentile")
    ax.plot(x, pct[50], linewidth=2, label="Median balance")
    ax.axhline(0, color="red", linestyle="--", linewidth=1, label="Overdrawn")
    ax.set_xticks(x)
    ax.set_xticklabels(MONTHS)
    ax.set_ylabel("End-of-month balance (GBP)")
    ax.set_title("Student cashflow stress test: 20,000 simulated years")
    ax.legend(loc="upper left")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def main() -> None:
    import argparse
    ap = argparse.ArgumentParser(description="Student cashflow Monte Carlo stress-tester")
    ap.add_argument("--hours", type=float, help="part-time hours per week")
    ap.add_argument("--savings", type=float, help="opening savings (GBP)")
    ap.add_argument("--rent", type=float, help="monthly rent (GBP)")
    ap.add_argument("--family", type=float, help="monthly family support (GBP)")
    ap.add_argument("--sims", type=int, default=20000, help="number of simulations")
    ap.add_argument("--plot", action="store_true", help="save stress_test.png")
    a = ap.parse_args()

    plan = Plan()
    if a.hours is not None:
        plan.hours_per_week = a.hours
    if a.savings is not None:
        plan.opening_savings = a.savings
    if a.rent is not None:
        plan.rent = a.rent
    if a.family is not None:
        plan.family_support_monthly = a.family

    balances = simulate(plan, a.sims)
    res = summarise(balances)
    print(f"Probability of ever being overdrawn: {res['p_ever_overdrawn']:.1%}")
    print(f"Most dangerous month: {res['worst_month']}")
    print(f"Buffer needed for 95% safety: GBP {res['buffer_for_95pct_safety']:.0f}")
    print("Month  P(overdrawn)  Median   10th pct")
    for m in MONTHS:
        print(f"{m:5s}  {res['p_overdrawn_by_month'][m]:11.1%}  "
              f"{res['median_balance'][m]:7.0f}  {res['p10_balance'][m]:8.0f}")
    print(f"Hours/week for <=5% risk: {hours_for_safety(plan):.1f}")
    if a.plot:
        plot(balances)
        print("Saved stress_test.png")


if __name__ == "__main__":
    main()
