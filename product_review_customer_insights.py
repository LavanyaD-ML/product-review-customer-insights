import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Project folder path
PROJECT_DIR = Path(__file__).resolve().parent

# Dataset path
DATA_FILE = PROJECT_DIR / "data" / "product_reviews.csv"

# Load dataset
df = pd.read_csv(DATA_FILE)

print("PRODUCT REVIEW DATA ANALYSIS & CUSTOMER INSIGHTS SYSTEM")
print("=" * 55)

print("\nDataset loaded successfully!")
print("\nFirst 5 records:")
print(df.head())

print("\nDataset Shape:")
print(df.shape)
print("\nDataset Information:")
df.info()

print("\nMissing Values:")
print(df.isnull().sum())
print("\nDuplicate Records:")
print(df.duplicated().sum())
print("\nRating Values Check:")
print(df["rating"].value_counts().sort_index())
print("\nInvalid Ratings Check:")
print(df[~df["rating"].between(1, 5)])
# Data Cleaning
df["product_name"] = df["product_name"].str.strip()
df["category"] = df["category"].str.strip()
df["review_text"] = df["review_text"].str.strip()

# Overall Rating Summary
print("\n--- Overall Rating Summary ---")
print(df["rating"].describe())

# Product-wise Analysis
product_summary = df.groupby("product_name").agg(
    Average_Rating=("rating", "mean"),
    Total_Reviews=("rating", "count")
).reset_index()

product_summary["Average_Rating"] = product_summary["Average_Rating"].round(2)

print("\n--- Product-wise Summary ---")
print(product_summary)

# Highest Rated Products
print("\n--- Highest Rated Products ---")
print(product_summary.sort_values(
    by="Average_Rating", ascending=False
))

# Lowest Rated Products
print("\n--- Lowest Rated Products ---")
print(product_summary.sort_values(
    by="Average_Rating", ascending=True
))

# Category-wise Analysis
print("\n--- Category-wise Summary ---")
print(df.groupby("category").agg(
    Average_Rating=("rating", "mean"),
    Total_Reviews=("rating", "count")
).round(2))

# Save Cleaned Dataset
df.to_csv(PROJECT_DIR / "data" / "cleaned_product_reviews.csv", index=False)

print("\nCleaned dataset saved successfully!")
# ==============================
# DATA VISUALIZATION
# ==============================

# 1. Rating Distribution Chart
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x="rating")
plt.title("Product Rating Distribution")
plt.xlabel("Rating")
plt.ylabel("Number of Reviews")
plt.tight_layout()
plt.savefig(PROJECT_DIR / "rating_distribution.png")
plt.close()

# 2. Product-wise Average Rating Chart
plt.figure(figsize=(9, 5))
sns.barplot(data=product_summary, x="product_name", y="Average_Rating")
plt.title("Average Rating by Product")
plt.xlabel("Product Name")
plt.ylabel("Average Rating")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(PROJECT_DIR / "product_ratings.png")
plt.close()

# 3. Category-wise Average Rating Chart
category_summary = df.groupby("category", as_index=False).agg(
    Average_Rating=("rating", "mean")
)

plt.figure(figsize=(8, 5))
sns.barplot(data=category_summary, x="category", y="Average_Rating")
plt.title("Average Rating by Category")
plt.xlabel("Category")
plt.ylabel("Average Rating")
plt.tight_layout()
plt.savefig(PROJECT_DIR / "category_ratings.png")
plt.close()

print("\nAll charts saved successfully!")


# ==============================
# SQL DATABASE
# ==============================

import sqlite3

DB_FILE = PROJECT_DIR / "product_reviews.db"

with sqlite3.connect(DB_FILE) as connection:
    df.to_sql(
        "product_reviews",
        connection,
        if_exists="replace",
        index=False
    )

    sql_summary = pd.read_sql_query(
        """
        SELECT
            product_name,
            ROUND(AVG(rating), 2) AS average_rating,
            COUNT(*) AS total_reviews
        FROM product_reviews
        GROUP BY product_name
        ORDER BY average_rating DESC
        """,
        connection
    )

    print("\n--- SQL Product Rating Summary ---")
    print(sql_summary)

print("\nSQL database created successfully!")
print("\nPROJECT ANALYSIS COMPLETED SUCCESSFULLY!")