# Pricing Strategy A/B Test Framework
### Pharmetric LLC | Statistical Measurement for Pricing Decisions

---

## Business Context

Before rolling out a new pricing strategy across a full account portfolio, a pharmaceutical distribution client ran a controlled pilot — applying the new strategy to 115 accounts while keeping 120 accounts on the existing pricing as a control. They needed a statistically rigorous framework to answer one question: **did the pricing change actually improve margin, or are we looking at random variation?**

This framework provides that answer with full statistical rigor, including significance testing, effect size quantification, confidence interval estimation, and a clear business recommendation.

---

## What This Framework Does

1. **Runs a two-sample Welch's t-test** to determine if the difference in mean margin between treatment and control groups is statistically significant
2. **Calculates Cohen's d effect size** to measure practical significance — because a statistically significant result can still be too small to matter commercially
3. **Constructs a 95% confidence interval** on the mean difference, giving leadership a realistic range for the true margin impact
4. **Projects annualized incremental margin** across the full treatment account base
5. **Issues a clear recommendation** — Proceed, Hold, or Halt — based on the statistical evidence

---

## Decision Framework

| Result | Recommendation |
|--------|---------------|
| Significant + positive + medium/large effect | ✅ Proceed with full rollout |
| Significant + positive + small effect | ⚠️ Consider — commercial value may be limited |
| Not significant | 🛑 Do not roll out — evidence insufficient |
| Significant + negative | 🚨 Halt — pricing strategy is detrimental |

---

## Methodology

- **Welch's t-test** (`scipy.stats.ttest_ind`) — used instead of standard t-test because group variances may differ
- **Cohen's d** — pooled standard deviation approach; thresholds: small (0.2), medium (0.5), large (0.8)
- **95% Confidence interval** — constructed using Welch-Satterthwaite degrees of freedom
- **Annualized lift** — mean difference × 12 months × number of treatment accounts

---

## How to Run

```bash
python pricing_ab_test.py
```

**Output files:**
- `ab_test_results.png` — distribution overlap + confidence interval chart
- `ab_test_results.csv` — full statistical results table

---

## Requirements

```
numpy
pandas
matplotlib
scipy
```

---

## Skills Demonstrated

`Hypothesis Testing` · `Two-Sample t-Test` · `Cohen's d Effect Size` · `Confidence Intervals` · `Statistical Significance` · `scipy.stats` · `numpy` · `matplotlib` · `Pricing Analytics` · `A/B Testing`

---

*Pharmetric LLC — Independent BI & Analytics Consulting*
*Enrique Esquivel | enrique.esquivel@protonmail.com*
