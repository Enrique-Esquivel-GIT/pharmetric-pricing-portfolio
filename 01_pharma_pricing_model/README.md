# Pharmaceutical Forward-Looking Pricing Model
### Pharmetric LLC | Strategic Pricing Analytics

---

## Business Context

A pharmaceutical distributor needed a systematic, data-driven approach to evaluate pricing decisions across its product portfolio before contract renewals and executive pricing reviews. The goal was to move from intuition-driven pricing to a model that quantifies the margin impact of price changes at the category level — Generic, Brand, and Specialty — over a 12-month forward horizon.

---

## What This Model Does

1. **Estimates price-volume relationships** using OLS regression on 24 months of historical pricing and volume data — producing price elasticity coefficients for each product category
2. **Projects 12-month forward margin** under three pricing scenarios: +5% increase, hold flat, -3% reduction
3. **Compares outcomes** across categories to identify where pricing power exists and where volume risk is highest
4. **Visualizes results** in an executive-ready bar chart and exports a structured CSV for further analysis

---

## Key Findings (Sample Output)

| Category  | Scenario       | Annual Margin |
|-----------|---------------|--------------|
| Generic   | Increase +5%  | Highest risk of volume loss — low elasticity floor |
| Brand     | Hold 0%       | Margin stable; limited upside from increases |
| Specialty | Increase +5%  | Highest margin leverage — inelastic demand |

*Actual output varies with data. Run the model to generate current projections.*

---

## Methodology

- **OLS Regression** (`statsmodels`) — price as independent variable, volume as dependent variable
- **Price Elasticity** — calculated as `b_price × (mean_price / mean_volume)`
- **Margin Projection** — `(New Price − COGS) × Projected Volume × 12 months`
- **Scenario logic** — applies multipliers to baseline price, re-estimates volume via regression coefficients

---

## How to Run

```bash
# 1. Generate synthetic dataset
python generate_data.py

# 2. Run the pricing model
python pricing_model.py
```

**Output files:**
- `scenario_comparison.png` — bar chart for executive presentation
- `pricing_scenario_results.csv` — full results table

---

## Requirements

```
pandas
numpy
matplotlib
statsmodels
```

---

## Skills Demonstrated

`OLS Regression` · `Price Elasticity` · `Scenario Analysis` · `Margin Modeling` · `pandas` · `statsmodels` · `matplotlib` · `Financial Analytics`

---

*Pharmetric LLC — Independent BI & Analytics Consulting*
*Enrique Esquivel | enrique.esquivel@protonmail.com*
