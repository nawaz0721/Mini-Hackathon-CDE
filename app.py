import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="E-commerce Products Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------
# LOAD DATA
# ---------------------------
@st.cache_data
def load_data():
    return pd.read_csv("./output/clean.csv")

df = load_data()

# ---------------------------
# HEADER
# ---------------------------
st.title("🛒 E-commerce Products Dashboard")
st.markdown("### Explore key insights from your product dataset")
st.divider()

# ---------------------------
# SIDEBAR MENU
# ---------------------------
st.sidebar.header("🔍 Select Analysis")
menu = st.sidebar.radio(
    "",
    ["Average Price by Category", "Rating vs Price", "Product Distribution by Category",
     "Reviews vs Price", "Number of Products by Rating"]
)

# ---------------------------
# CHART RENDER FUNCTION
# ---------------------------
def show_chart(fig):
    st.pyplot(fig)
    st.divider()

# ---------------------------
# ANALYSIS 1 — Average Price by Category
# ---------------------------
if menu == "Average Price by Category":
    st.header("📊 Average Product Price by Price Category")

    result = df.groupby('price_category')['price'].mean().sort_values()

    col1, col2 = st.columns([1,1])

    # Left = Table
    with col1:
        st.subheader("Table")
        st.dataframe(result, use_container_width=True)

    # Right = Chart
    with col2:
        st.subheader("Bar Chart")
        fig, ax = plt.subplots(figsize=(10,6))
        result.plot(kind='bar', color='skyblue', ax=ax)
        ax.set_xlabel("Price Category")
        ax.set_ylabel("Average Price")
        ax.set_title("Average Product Price by Category")
        show_chart(fig)

# ---------------------------
# ANALYSIS 2 — Rating vs Price
# ---------------------------
elif menu == "Rating vs Price":
    st.header("⭐ Rating vs Price")

    col1, col2 = st.columns([1,1])

    with col1:
        st.subheader("Sample Data")
        st.dataframe(df[['rating','price']].head(20), use_container_width=True)

    with col2:
        st.subheader("Scatter Plot")
        fig, ax = plt.subplots(figsize=(8,6))
        ax.scatter(df['rating'], df['price'], alpha=0.6)
        ax.set_xlabel("Rating")
        ax.set_ylabel("Price")
        ax.set_title("Rating vs Price")
        show_chart(fig)

# ---------------------------
# ANALYSIS 3 — Product Distribution by Category
# ---------------------------
elif menu == "Product Distribution by Category":
    st.header("📊 Product Distribution by Price Category")

    counts = df['price_category'].value_counts()

    col1, col2 = st.columns([1,1])

    with col1:
        st.subheader("Table")
        st.dataframe(counts, use_container_width=True)

    with col2:
        st.subheader("Pie Chart")
        fig, ax = plt.subplots(figsize=(7,7))
        counts.plot(kind='pie', autopct='%1.1f%%', colors=['lightgreen','lightblue','salmon'], ax=ax, startangle=90)
        ax.set_ylabel("")
        ax.set_title("Product Distribution by Price Category")
        show_chart(fig)

# ---------------------------
# ANALYSIS 4 — Reviews vs Price
# ---------------------------
elif menu == "Reviews vs Price":
    st.header("📝 Reviews vs Price")

    col1, col2 = st.columns([1,1])

    with col1:
        st.subheader("Sample Data")
        st.dataframe(df[['reviews','price']].head(20), use_container_width=True)

    with col2:
        st.subheader("Scatter Plot")
        fig, ax = plt.subplots(figsize=(8,6))
        ax.scatter(df['reviews'], df['price'], alpha=0.6, color='orange')
        ax.set_xlabel("Number of Reviews")
        ax.set_ylabel("Price")
        ax.set_title("Reviews vs Price")
        show_chart(fig)

# ---------------------------
# ANALYSIS 5 — Number of Products by Rating
# ---------------------------
elif menu == "Number of Products by Rating":
    st.header("⭐ Number of Products by Rating")

    counts = df['rating'].value_counts().sort_index()

    col1, col2 = st.columns([1,1])

    with col1:
        st.subheader("Table")
        st.dataframe(counts, use_container_width=True)

    with col2:
        st.subheader("Bar Chart")
        fig, ax = plt.subplots(figsize=(10,6))
        counts.plot(kind='bar', color='purple', ax=ax)
        ax.set_xlabel("Rating")
        ax.set_ylabel("Count")
        ax.set_title("Number of Products by Rating")
        show_chart(fig)
