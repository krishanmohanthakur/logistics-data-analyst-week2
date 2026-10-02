"""
Yuva Intern - Week 2
Data Collection, Cleaning and Preprocessing for Logistics Analysis
Dataset: Brazilian E-Commerce Public Dataset by Olist
"""

import pandas as pd
import numpy as np
from pathlib import Path

DATA_DIR = Path("data")

# 1. Load datasets
orders = pd.read_csv(DATA_DIR / "olist_orders_dataset.csv")
items = pd.read_csv(DATA_DIR / "olist_order_items_dataset.csv")
reviews = pd.read_csv(DATA_DIR / "olist_order_reviews_dataset.csv")
products = pd.read_csv(DATA_DIR / "olist_products_dataset.csv")

# 2. Basic quality checks
print("Orders:", orders.shape)
print("Items:", items.shape)
print("Reviews:", reviews.shape)
print("Products:", products.shape)

print("\nMissing values - orders:")
print(orders.isna().sum()[orders.isna().sum() > 0])

# 3. Convert date fields safely
date_cols = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]
for col in date_cols:
    orders[col] = pd.to_datetime(orders[col], errors="coerce")

# 4. Handle missing review text
# Missing text means the customer did not provide that field;
# it should not be treated as a numeric missing value.
reviews["review_comment_title"] = reviews["review_comment_title"].fillna("No comment")
reviews["review_comment_message"] = reviews["review_comment_message"].fillna("No comment")

# 5. Handle product attributes
products["product_category_name"] = products["product_category_name"].fillna("Unknown")
for col in ["product_weight_g", "product_length_cm",
            "product_height_cm", "product_width_cm"]:
    products[col] = products[col].fillna(products[col].median())

# 6. Create logistics features
orders["delivery_time_days"] = (
    orders["order_delivered_customer_date"]
    - orders["order_purchase_timestamp"]
).dt.total_seconds() / 86400

orders["delivery_delay_days"] = (
    orders["order_delivered_customer_date"]
    - orders["order_estimated_delivery_date"]
).dt.total_seconds() / 86400

# 7. Outlier detection using IQR (flag first; do not blindly delete)
def iqr_flags(series):
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    return (series < lower) | (series > upper), lower, upper

items["price_outlier"], price_low, price_high = iqr_flags(items["price"])
items["freight_outlier"], freight_low, freight_high = iqr_flags(items["freight_value"])

orders["delivery_outlier"], delivery_low, delivery_high = iqr_flags(
    orders["delivery_time_days"].dropna()
)
# Because the last expression returns a Series indexed only on non-null rows,
# assign the flags back by index for safety.
orders["delivery_outlier"] = False
valid_idx = orders["delivery_time_days"].dropna().index
flags, _, _ = iqr_flags(orders.loc[valid_idx, "delivery_time_days"])
orders.loc[valid_idx, "delivery_outlier"] = flags

# 8. Min-Max normalization
for col in ["price", "freight_value"]:
    mn, mx = items[col].min(), items[col].max()
    items[col + "_normalized"] = (items[col] - mn) / (mx - mn)

# 9. Remove exact duplicate rows only where appropriate.
# Keep business-level repeated transactions unless they violate a key.
orders = orders.drop_duplicates()
items = items.drop_duplicates()

# 10. Save prepared files
Path("output").mkdir(exist_ok=True)
orders.to_csv("output/orders_preprocessed.csv", index=False)
items.to_csv("output/order_items_preprocessed.csv", index=False)
reviews.to_csv("output/order_reviews_preprocessed.csv", index=False)
products.to_csv("output/products_preprocessed.csv", index=False)

print("\nPreprocessing completed.")
