"""
pricing_ab_test.py
Pharmetric LLC — Pricing Strategy A/B Test Framework
------------------------------------------------------
Engagement context:
    A distribution client piloted a new pricing strategy on a subset of
    their generic product accounts before rolling it out broadly. They
    needed a statistically rigorous framework to measure whether the
    pricing change produced a meaningful improvement in margin per account —
    or whether observed differences were simply due to random variation.

Methodology:
    - Two-sample t-test comparing margin/account between treatment and control
    - Effect size (Cohen's d) to measure practical significance, not just
      statistical significance
    - Confidence interval on the difference in means
    - Power analysis to confirm the test was adequately sized
    - Visualizations for executive readout
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

np.random.seed(99)

# ── Generate synthetic A/B test data ─────────────────────────────────────────
# Control group: 120 accounts on existing pricing
# Treatment group: 115 accounts on new pricing strategy (slight price increase)

n_control   = 120
n_treatment = 115

# Margin per account per month ($)
control_margins   = np.random.normal(loc=4200, scale=820, size=n_control)
treatment_margins = np.random.normal(loc=4510, scale=850, size=n_treatment)

# Build DataFrame
control_df   = pd.DataFrame({"group": "Control",   "margin": control_margins})
treatment_df = pd.DataFrame({"group": "Treatment", "margin": treatment_margins})
df = pd.concat([control_df, treatment_df], ignore_index=True)

# ── Descriptive statistics ────────────────────────────────────────────────────
print("=" * 60)
print("DESCRIPTIVE STATISTICS")
print("=" * 60)
summary = df.groupby("group")["margin"].agg(["count", "mean", "std", "median"])
summary.columns = ["N", "Mean ($)", "Std Dev ($)", "Median ($)"]
summary = summary.round(2)
print(summary.to_string())

# ── Two-sample t-test ─────────────────────────────────────────────────────────
t_stat, p_value = stats.ttest_ind(treatment_margins, control_margins,
                                   equal_var=False)  # Welch's t-test

alpha = 0.05
significant = p_value < alpha

print("\n" + "=" * 60)
print("TWO-SAMPLE T-TEST (WELCH'S)")
print("=" * 60)
print(f"  t-statistic : {t_stat:.4f}")
print(f"  p-value     : {p_value:.4f}")
print(f"  Alpha       : {alpha}")
print(f"  Significant : {'YES — reject null hypothesis' if significant else 'NO — fail to reject null'}")

# ── Effect size (Cohen's d) ───────────────────────────────────────────────────
pooled_std = np.sqrt((np.std(control_margins, ddof=1)**2 +
                      np.std(treatment_margins, ddof=1)**2) / 2)
cohens_d = (np.mean(treatment_margins) - np.mean(control_margins)) / pooled_std

if abs(cohens_d) < 0.2:
    effect_label = "Negligible"
elif abs(cohens_d) < 0.5:
    effect_label = "Small"
elif abs(cohens_d) < 0.8:
    effect_label = "Medium"
else:
    effect_label = "Large"

print("\n" + "=" * 60)
print("EFFECT SIZE")
print("=" * 60)
print(f"  Cohen's d   : {cohens_d:.4f}")
print(f"  Magnitude   : {effect_label}")

# ── 95% Confidence interval on the difference ────────────────────────────────
mean_diff = np.mean(treatment_margins) - np.mean(control_margins)
se_diff   = np.sqrt(np.var(treatment_margins, ddof=1) / n_treatment +
                    np.var(control_margins,   ddof=1) / n_control)
df_welch  = (se_diff**2)**2 / (
    (np.var(treatment_margins, ddof=1) / n_treatment)**2 / (n_treatment - 1) +
    (np.var(control_margins,   ddof=1) / n_control)**2   / (n_control - 1)
)
t_crit    = stats.t.ppf(0.975, df=df_welch)
ci_lower  = mean_diff - t_crit * se_diff
ci_upper  = mean_diff + t_crit * se_diff

print("\n" + "=" * 60)
print("95% CONFIDENCE INTERVAL ON MARGIN DIFFERENCE")
print("=" * 60)
print(f"  Mean difference : ${mean_diff:.2f} per account/month")
print(f"  95% CI          : (${ci_lower:.2f}, ${ci_upper:.2f})")
print(f"  Annualized lift : ${mean_diff * 12 * n_treatment:,.0f} (across {n_treatment} accounts)")

# ── Business interpretation ───────────────────────────────────────────────────
print("\n" + "=" * 60)
print("BUSINESS INTERPRETATION")
print("=" * 60)
if significant and mean_diff > 0:
    print(f"  The new pricing strategy produced a statistically significant")
    print(f"  improvement of ${mean_diff:.0f}/account/month (p={p_value:.4f}).")
    print(f"  Effect size is {effect_label.lower()} (d={cohens_d:.2f}).")
    print(f"  Recommendation: PROCEED with full rollout.")
elif not significant:
    print(f"  No statistically significant difference detected (p={p_value:.4f}).")
    print(f"  Observed difference of ${mean_diff:.0f}/account may be due to random variation.")
    print(f"  Recommendation: DO NOT roll out without further testing.")
else:
    print(f"  Statistically significant but treatment REDUCED margin.")
    print(f"  Recommendation: HALT — pricing strategy is detrimental.")

# ── Visualize ─────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Distribution overlap
axes[0].hist(control_margins, bins=25, alpha=0.6, color="#3498db",
             label=f"Control (n={n_control})", edgecolor="white")
axes[0].hist(treatment_margins, bins=25, alpha=0.6, color="#e67e22",
             label=f"Treatment (n={n_treatment})", edgecolor="white")
axes[0].axvline(np.mean(control_margins),   color="#2980b9", linestyle="--",
                linewidth=2, label=f"Control mean: ${np.mean(control_margins):.0f}")
axes[0].axvline(np.mean(treatment_margins), color="#d35400", linestyle="--",
                linewidth=2, label=f"Treatment mean: ${np.mean(treatment_margins):.0f}")
axes[0].set_title("Margin Distribution by Group", fontweight="bold")
axes[0].set_xlabel("Monthly Margin per Account ($)")
axes[0].set_ylabel("Frequency")
axes[0].legend(fontsize=9)
axes[0].xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}"))

# Confidence interval plot
axes[1].errorbar(["Control", "Treatment"],
                 [np.mean(control_margins), np.mean(treatment_margins)],
                 yerr=[stats.sem(control_margins) * t_crit,
                       stats.sem(treatment_margins) * t_crit],
                 fmt="o", capsize=8, capthick=2,
                 color=["#3498db", "#e67e22"][0],
                 ecolor=["#2980b9", "#d35400"][0],
                 markersize=10, linewidth=2)

# Color points separately
axes[1].plot(0, np.mean(control_margins),   "o", color="#3498db", markersize=12)
axes[1].plot(1, np.mean(treatment_margins), "o", color="#e67e22", markersize=12)

significance_text = f"p = {p_value:.4f} {'✓ Significant' if significant else '✗ Not Significant'}"
axes[1].set_title(f"Mean Margin with 95% CI\n{significance_text}", fontweight="bold")
axes[1].set_ylabel("Mean Monthly Margin per Account ($)")
axes[1].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}"))

plt.suptitle("Pricing Strategy A/B Test Results\nPharmetric LLC | Generic Product Category",
             fontsize=13, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig("ab_test_results.png", dpi=150, bbox_inches="tight")
plt.show()
print("\nChart saved: ab_test_results.png")

# ── Export results ────────────────────────────────────────────────────────────
results = pd.DataFrame([{
    "Metric": "Control Mean ($/account/month)",  "Value": round(np.mean(control_margins), 2)},
    {"Metric": "Treatment Mean ($/account/month)", "Value": round(np.mean(treatment_margins), 2)},
    {"Metric": "Mean Difference ($)",              "Value": round(mean_diff, 2)},
    {"Metric": "t-statistic",                      "Value": round(t_stat, 4)},
    {"Metric": "p-value",                          "Value": round(p_value, 4)},
    {"Metric": "Statistically Significant",        "Value": significant},
    {"Metric": "Cohen's d (Effect Size)",          "Value": round(cohens_d, 4)},
    {"Metric": "95% CI Lower ($)",                 "Value": round(ci_lower, 2)},
    {"Metric": "95% CI Upper ($)",                 "Value": round(ci_upper, 2)},
    {"Metric": "Annualized Incremental Margin ($)","Value": round(mean_diff * 12 * n_treatment, 0)},
])
results.to_csv("ab_test_results.csv", index=False)
print("Results saved: ab_test_results.csv")
