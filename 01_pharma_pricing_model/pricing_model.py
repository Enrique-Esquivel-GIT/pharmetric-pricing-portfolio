"""
pricing_model.py
Pharmetric LLC — Forward-Looking Pharmaceutical Pricing Model
---------------------------------------------------------------
Engagement context:
    A regional pharmaceutical distributor engaged Pharmetric LLC to build
    a forward-looking pricing model across three product categories:
    Generic, Brand, and Specialty. The objective was to quantify the
    margin impact of pricing decisions over a 12-month horizon and support
    executive-level pricing strategy reviews.

Methodology:
    - OLS regression to estimate price-volume relationships per category
    - Scenario analysis: price increase (+5%), hold (0%), reduction (-3%)
    - Margin projection: (Price - COGS) × Projected Volume
    - Visualizations for executive presentation
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm

# ── Load historical data ──────────────────────────────────────────────────────
df = pd.read_csv("pricing_data.csv")

categories = ["generic", "brand", "specialty"]

# ── Step 1: Estimate price-volume relationship per category ───────────────────
# Using OLS: Volume = b0 + b1 * Price
# This gives us the slope we need to project volume at new price points.

models = {}
print("=" * 60)
print("PRICE-VOLUME ELASTICITY ESTIMATES")
print("=" * 60)

for cat in categories:
    X = sm.add_constant(df[f"price_{cat}"])
    y = df[f"volume_{cat}"]
    model = sm.OLS(y, X).fit()
    models[cat] = model

    b_price = model.params[f"price_{cat}"]
    mean_p = df[f"price_{cat}"].mean()
    mean_q = df[f"volume_{cat}"].mean()
    elasticity = b_price * (mean_p / mean_q)

    print(f"\n{cat.capitalize()}")
    print(f"  Price coefficient : {b_price:.2f}")
    print(f"  R-squared         : {model.rsquared:.3f}")
    print(f"  Price elasticity  : {elasticity:.3f}")

# ── Step 2: Define pricing scenarios ─────────────────────────────────────────
scenarios = {
    "Increase (+5%)": 1.05,
    "Hold (0%)":      1.00,
    "Reduce (-3%)":   0.97,
}

# Baseline: use last month's observed values
baseline = {cat: {
    "price": df[f"price_{cat}"].iloc[-1],
    "cogs":  df[f"cogs_{cat}"].iloc[-1],
    "volume": df[f"volume_{cat}"].iloc[-1],
} for cat in categories}

# ── Step 3: Project 12-month forward margin per scenario ─────────────────────
horizon = 12
results = []

for cat in categories:
    model = models[cat]
    base_price = baseline[cat]["price"]
    base_cogs  = baseline[cat]["cogs"]
    b0 = model.params["const"]
    b1 = model.params[f"price_{cat}"]

    for scenario_name, multiplier in scenarios.items():
        new_price = base_price * multiplier

        # Project volume using OLS coefficients
        projected_volume = max(b0 + b1 * new_price, 0)

        # Margin per unit and total monthly margin
        margin_per_unit   = new_price - base_cogs
        monthly_margin    = margin_per_unit * projected_volume
        annual_margin     = monthly_margin * horizon
        margin_pct        = (margin_per_unit / new_price) * 100

        results.append({
            "Category":          cat.capitalize(),
            "Scenario":          scenario_name,
            "New Price":         round(new_price, 2),
            "COGS":              round(base_cogs, 2),
            "Margin/Unit":       round(margin_per_unit, 2),
            "Margin %":          round(margin_pct, 1),
            "Projected Volume":  int(projected_volume),
            "Monthly Margin $":  round(monthly_margin, 0),
            "Annual Margin $":   round(annual_margin, 0),
        })

results_df = pd.DataFrame(results)

print("\n\n" + "=" * 60)
print("12-MONTH FORWARD PRICING SCENARIO PROJECTIONS")
print("=" * 60)
print(results_df.to_string(index=False))

# ── Step 4: Visualize scenario comparison ────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(16, 6), sharey=False)
colors = {"Increase (+5%)": "#2ecc71", "Hold (0%)": "#3498db", "Reduce (-3%)": "#e74c3c"}

for i, cat in enumerate(categories):
    cat_data = results_df[results_df["Category"] == cat.capitalize()]
    bars = axes[i].bar(
        cat_data["Scenario"],
        cat_data["Annual Margin $"] / 1_000_000,
        color=[colors[s] for s in cat_data["Scenario"]],
        edgecolor="white", linewidth=0.8
    )
    axes[i].set_title(f"{cat.capitalize()} Category", fontsize=13, fontweight="bold")
    axes[i].set_ylabel("Annual Margin ($M)" if i == 0 else "")
    axes[i].set_xlabel("Pricing Scenario")
    axes[i].tick_params(axis="x", labelsize=9)
    axes[i].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:.1f}M"))

    # Label bars
    for bar, val in zip(bars, cat_data["Annual Margin $"]):
        axes[i].text(bar.get_x() + bar.get_width() / 2,
                     bar.get_height() + 0.01,
                     f"${val/1_000_000:.2f}M",
                     ha="center", va="bottom", fontsize=9, fontweight="bold")

plt.suptitle("12-Month Margin Projections by Pricing Scenario\nPharmetric LLC | Pharmaceutical Pricing Analysis",
             fontsize=14, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig("scenario_comparison.png", dpi=150, bbox_inches="tight")
plt.show()
print("\nChart saved: scenario_comparison.png")

# ── Step 5: Export results ────────────────────────────────────────────────────
results_df.to_csv("pricing_scenario_results.csv", index=False)
print("Results saved: pricing_scenario_results.csv")
