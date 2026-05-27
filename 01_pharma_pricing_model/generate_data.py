"""
generate_data.py
Pharmetric LLC — Pharmaceutical Pricing Model
Generates synthetic pharma pricing and volume data for modeling.
"""

import pandas as pd
import numpy as np

np.random.seed(42)
months = 24

data = pd.DataFrame({
    "month": range(1, months + 1),

    # Generic category: price-sensitive, high volume
    "price_generic":    np.round(np.linspace(10.00, 11.50, months) + np.random.normal(0, 0.2, months), 2),
    "volume_generic":   np.round(5000 - 120 * np.linspace(0, 1.5, months) + np.random.normal(0, 80, months)).astype(int),
    "cogs_generic":     np.round(np.linspace(5.50, 6.00, months) + np.random.normal(0, 0.1, months), 2),

    # Brand category: moderate price sensitivity, mid volume
    "price_brand":      np.round(np.linspace(85.00, 91.00, months) + np.random.normal(0, 1.2, months), 2),
    "volume_brand":     np.round(1200 - 20 * np.linspace(0, 6.0, months) + np.random.normal(0, 30, months)).astype(int),
    "cogs_brand":       np.round(np.linspace(42.00, 44.50, months) + np.random.normal(0, 0.5, months), 2),

    # Specialty category: low price sensitivity, low volume, high margin
    "price_specialty":  np.round(np.linspace(310.00, 330.00, months) + np.random.normal(0, 4.0, months), 2),
    "volume_specialty": np.round(300 - 2 * np.linspace(0, 20.0, months) + np.random.normal(0, 10, months)).astype(int),
    "cogs_specialty":   np.round(np.linspace(120.00, 128.00, months) + np.random.normal(0, 2.0, months), 2),
})

data.to_csv("pricing_data.csv", index=False)
print("pricing_data.csv generated successfully.")
print(data.head())
