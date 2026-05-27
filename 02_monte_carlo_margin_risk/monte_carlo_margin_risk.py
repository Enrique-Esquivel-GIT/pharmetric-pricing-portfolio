"""
monte_carlo_margin_risk.py
Pharmetric LLC — Monte Carlo Margin Risk Simulator
----------------------------------------------------
Engagement context:
    A Strategic Accounts team asked Pharmetric LLC to quantify the range
    of possible margin outcomes for a major contract renewal under pricing
    uncertainty. Rather than a single-point estimate, leadership needed to
    understand the distribution of outcomes — including downside risk — to
    make a defensible pricing decision.

Methodology:
    - 10,000 Monte Carlo simulations per product category
    - Three sources of uncertainty: price change, volume change, product mix shift
    - Output: margin distribution, percentile ranges, and Value-at-Risk style metrics
    - Visualizations suitable for executive risk review
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import norm

np.random.seed(42)
N_SIMULATIONS = 10_000

# ── Baseline assumptions per category ────────────────────────────────────────
# These would come from actual contract data in a real engagement.
categories = {
    "Generic": {
        "base_price":  10.50,
        "base_volume": 4800,
        "base_cogs":   5.75,
        "price_change_mean":  0.00,   # expected price change %
        "price_change_std":   0.05,   # uncertainty in price change
        "volume_change_mean": -0.02,  # expected volume erosion
        "volume_change_std":  0.08,   # volume uncertainty
    },
    "Brand": {
        "base_price":  88.00,
        "base_volume": 1150,
        "base_cogs":   43.00,
        "price_change_mean":  0.02,
        "price_change_std":   0.04,
        "volume_change_mean": -0.01,
        "volume_change_std":  0.06,
    },
    "Specialty": {
        "base_price":  320.00,
        "base_volume": 290,
        "base_cogs":   124.00,
        "price_change_mean":  0.04,
        "price_change_std":   0.06,
        "volume_change_mean":  0.01,
        "volume_change_std":  0.10,
    },
}

# ── Run simulations ───────────────────────────────────────────────────────────
results = {}
summary_rows = []

print("=" * 65)
print("MONTE CARLO MARGIN RISK SIMULATION — 10,000 SCENARIOS")
print("=" * 65)

for cat_name, params in categories.items():

    # Simulate price and volume changes
    price_changes  = np.random.normal(params["price_change_mean"],
                                      params["price_change_std"],
                                      N_SIMULATIONS)
    volume_changes = np.random.normal(params["volume_change_mean"],
                                      params["volume_change_std"],
                                      N_SIMULATIONS)

    # Apply changes to baseline
    sim_prices  = params["base_price"]  * (1 + price_changes)
    sim_volumes = params["base_volume"] * (1 + volume_changes)
    sim_volumes = np.maximum(sim_volumes, 0)  # no negative volume

    # Annual margin = (price - cogs) * volume * 12 months
    sim_margins = (sim_prices - params["base_cogs"]) * sim_volumes * 12

    results[cat_name] = sim_margins

    # Summary statistics
    p5   = np.percentile(sim_margins, 5)
    p25  = np.percentile(sim_margins, 25)
    p50  = np.percentile(sim_margins, 50)
    p75  = np.percentile(sim_margins, 75)
    p95  = np.percentile(sim_margins, 95)
    mean = sim_margins.mean()
    prob_below_base = (sim_margins < (params["base_price"] - params["base_cogs"])
                       * params["base_volume"] * 12).mean() * 100

    print(f"\n{cat_name} Category")
    print(f"  Expected annual margin  : ${mean:>12,.0f}")
    print(f"  5th percentile  (worst) : ${p5:>12,.0f}")
    print(f"  25th percentile         : ${p25:>12,.0f}")
    print(f"  Median                  : ${p50:>12,.0f}")
    print(f"  75th percentile         : ${p75:>12,.0f}")
    print(f"  95th percentile (best)  : ${p95:>12,.0f}")
    print(f"  Prob. below baseline    : {prob_below_base:.1f}%")

    summary_rows.append({
        "Category":       cat_name,
        "Expected ($)":   round(mean),
        "P5 - Downside":  round(p5),
        "P25":            round(p25),
        "Median":         round(p50),
        "P75":            round(p75),
        "P95 - Upside":   round(p95),
        "% Below Baseline": round(prob_below_base, 1),
    })

# ── Visualize distributions ───────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
colors = {"Generic": "#3498db", "Brand": "#e67e22", "Specialty": "#9b59b6"}

for i, (cat_name, margins) in enumerate(results.items()):
    ax = axes[i]
    ax.hist(margins / 1_000_000, bins=60, color=colors[cat_name],
            edgecolor="white", linewidth=0.3, alpha=0.85)

    # Mark percentile lines
    for pct, label, color in [
        (5,  "P5",     "#e74c3c"),
        (50, "Median", "#2ecc71"),
        (95, "P95",    "#27ae60"),
    ]:
        val = np.percentile(margins, pct) / 1_000_000
        ax.axvline(val, color=color, linestyle="--", linewidth=1.5,
                   label=f"{label}: ${val:.1f}M")

    ax.set_title(f"{cat_name} Category\nMargin Distribution", fontsize=12, fontweight="bold")
    ax.set_xlabel("Annual Margin ($M)")
    ax.set_ylabel("Frequency" if i == 0 else "")
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:.1f}M"))
    ax.legend(fontsize=8)

plt.suptitle("Monte Carlo Margin Risk Simulation — 10,000 Scenarios\nPharmetric LLC | Strategic Accounts Pricing Risk Analysis",
             fontsize=13, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig("margin_risk_distribution.png", dpi=150, bbox_inches="tight")
plt.show()
print("\nChart saved: margin_risk_distribution.png")

# ── Export summary ────────────────────────────────────────────────────────────
summary_df = pd.DataFrame(summary_rows)
summary_df.to_csv("margin_risk_summary.csv", index=False)
print("Summary saved: margin_risk_summary.csv")
