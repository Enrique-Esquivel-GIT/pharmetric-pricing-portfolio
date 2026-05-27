# Monte Carlo Margin Risk Simulation
### Pharmetric LLC | Strategic Accounts Pricing Risk Analysis

---

## Business Context

When a Strategic Accounts team faces a contract renewal, a single-point margin estimate isn't enough. Price changes, volume shifts, and product mix uncertainty all interact — and the difference between the 5th and 95th percentile outcome can be tens of millions of dollars. Leadership needed a probabilistic view of margin outcomes to make a defensible pricing decision with confidence.

Pharmetric LLC built this Monte Carlo simulation to quantify that uncertainty and give the pricing team a clear picture of downside risk, expected value, and upside potential across three product categories.

---

## What This Model Does

1. **Simulates 10,000 pricing scenarios** per category, drawing price and volume changes from normal distributions calibrated to historical volatility
2. **Calculates the full distribution** of annual margin outcomes for Generic, Brand, and Specialty product categories
3. **Reports percentile ranges** (P5 through P95) so leadership understands not just the expected outcome but the realistic downside and upside
4. **Flags probability of falling below baseline** — a key risk metric for contract negotiation

---

## Key Risk Metrics (Sample)

| Category  | P5 (Downside) | Expected | P95 (Upside) | % Below Baseline |
|-----------|-------------|---------|------------|----------------|
| Generic   | Lowest      | Moderate | Capped by elasticity | Highest |
| Brand     | Moderate    | Strong   | Good upside | Low |
| Specialty | Highest floor| Best    | Significant upside | Lowest |

*Run the model for actual figures against your data.*

---

## Methodology

- **Monte Carlo simulation** — 10,000 draws per category using `numpy.random.normal`
- **Uncertainty sources** — price change %, volume change % (independently simulated)
- **Annual margin** — `(Price − COGS) × Volume × 12`
- **Risk metrics** — percentile analysis (P5, P25, P50, P75, P95), probability of underperformance

---

## How to Run

```bash
python monte_carlo_margin_risk.py
```

**Output files:**
- `margin_risk_distribution.png` — distribution chart with percentile markers
- `margin_risk_summary.csv` — full percentile summary table

---

## Requirements

```
numpy
matplotlib
pandas
scipy
```

---

## Skills Demonstrated

`Monte Carlo Simulation` · `Risk Quantification` · `Probability Distributions` · `Percentile Analysis` · `numpy` · `matplotlib` · `scipy` · `Pricing Risk Management`

---

*Pharmetric LLC — Independent BI & Analytics Consulting*
*Enrique Esquivel | enrique.esquivel@protonmail.com*
