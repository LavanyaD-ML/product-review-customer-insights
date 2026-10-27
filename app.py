import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(
    page_title="Product Review Customer Insights",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Product Review Data Analysis & Customer Insights")
st.write("Analyze product ratings, customer reviews, and category performance.")

# Load dataset
data_path = Path("Product Reviews.csv")
cleaned_path = Path("CLEAN Product Reviews.csv")
db_path = Path("Product Review.db")

uploaded_file = st.sidebar.file_uploader(
    "Upload Product Reviews CSV",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
elif cleaned_path.exists():
    df = pd.read_csv(cleaned_path)
elif data_path.exists():
    df = pd.read_csv(data_path)
else:
    st.warning("Please upload your Product Reviews CSV file.")
    st.stop()

df.columns = df.columns.str.strip()

st.sidebar.header("Dashboard Navigation")
page = st.sidebar.radio(
    "Select Page",
    ["Overview", "Product Analysis", "Category Analysis", "Rating Distribution", "Data"]
)

st.subheader("Dataset Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Reviews", len(df))

if "rating" in df.columns:
    col2.metric("Average Rating", f"{df['rating'].mean():.2f} / 5")
else:
    col2.metric("Average Rating", "N/A")

if "product_name" in df.columns:
    col3.metric("Products", df["product_name"].nunique())
else:
    col3.metric("Products", "N/A")

if page == "Overview":
    st.subheader("Recent Reviews")
    st.dataframe(df.head(10), use_container_width=True)

elif page == "Product Analysis":
    if {"product_name", "rating"}.issubset(df.columns):
        summary = (
            df.groupby("product_name")["rating"]
            .agg(["mean", "count"])
            .reset_index()
        )
        summary.columns = ["Product", "Average Rating", "Total Reviews"]

        st.dataframe(summary, use_container_width=True)

        fig, ax = plt.subplots()
        ax.bar(summary["Product"], summary["Average Rating"])
        ax.set_ylabel("Average Rating")
        ax.set_xlabel("Product")
        ax.set_title("Average Rating by Product")
        ax.tick_params(axis="x", rotation=45)
        st.pyplot(fig)
    else:
        st.warning("Required columns: product_name and rating.")

elif page == "Category Analysis":
    if {"category", "rating"}.issubset(df.columns):
        summary = df.groupby("category")["rating"].mean().reset_index()
        summary.columns = ["Category", "Average Rating"]

        st.dataframe(summary, use_container_width=True)

        fig, ax = plt.subplots()
        ax.bar(summary["Category"], summary["Average Rating"])
        ax.set_ylabel("Average Rating")
        ax.set_title("Average Rating by Category")
        st.pyplot(fig)
    else:
        st.warning("Required columns: category and rating.")

elif page == "Rating Distribution":
    if "rating" in df.columns:
        counts = df["rating"].value_counts().sort_index()

        fig, ax = plt.subplots()
        ax.bar(counts.index.astype(str), counts.values)
        ax.set_xlabel("Rating")
        ax.set_ylabel("Number of Reviews")
        ax.set_title("Rating Distribution")
        st.pyplot(fig)
    else:
        st.warning("Rating column not found.")

elif page == "Data":
    st.subheader("Full Dataset")
    st.dataframe(df, use_container_width=True)

    st.download_button(
        "Download Dataset",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="product_reviews.csv",
        mime="text/csv"
    )