import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------------------------------
# PAGE CONFIG (Modern Theme)
# ----------------------------------------------------
st.set_page_config(
    page_title="E-Commerce Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Modern CSS styling
st.markdown("""
<style>
/* General */
html, body, [class*="css"] {
    font-family: "Helvetica Neue", sans-serif;
}

/* Header Title */
.title {
    font-size: 40px;
    font-weight: 700;
    color: #333333;
}

/* Section Headers */
.section-header {
    font-size: 28px;
    font-weight: 600;
    color: #444;
    margin-top: 15px;
    padding-bottom: 5px;
    border-bottom: 2px solid #eee;
}

/* Divider style */
hr {
    border: none;
    height: 2px;
    background: #efefef;
    margin: 20px 0;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #f8f9fa;
    border-right: 1px solid #e6e6e6;
}

/* Metric Cards */
.metric-card {
    background: #ffffff;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
    text-align: center;
    margin-bottom: 20px;
}

.metric-value {
    font-size: 28px;
    font-weight: 700;
    color: #2c3e50;
}

.metric-label {
    font-size: 14px;
    color: #7f8c8d;
}
</style>
""", unsafe_allow_html=True)


# ----------------------------------------------------
# LOAD DATA
# ----------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("./output/clean.csv")

df = load_data()

# ----------------------------------------------------
# HEADER
# ----------------------------------------------------
st.markdown('<div class="title">📊 E-Commerce Analytics Dashboard</div>', unsafe_allow_html=True)
st.markdown("Gain powerful insights from your product dataset using interactive visualizations.")
st.markdown("<hr>", unsafe_allow_html=True)

# ----------------------------------------------------
# SIDEBAR MENU
# ----------------------------------------------------
st.sidebar.markdown("### 📌 Analysis Menu")
menu = st.sidebar.radio(
    "",
    [
        "Average Price by Category",
        "Rating vs Price",
        "Product Distribution by Category",
        "Reviews vs Price",
        "Number of Products by Rating"
    ]
)

# ----------------------------------------------------
# KPI METRICS ROW
# ----------------------------------------------------
colA, colB, colC, colD = st.columns(4)

with colA:
    st.markdown('<div class="metric-card"><div class="metric-value">'
                f'{df["price"].mean():.2f}'
                '</div><div class="metric-label">Avg Price</div></div>', unsafe_allow_html=True)

with colB:
    st.markdown('<div class="metric-card"><div class="metric-value">'
                f'{df["rating"].mean():.2f}'
                '</div><div class="metric-label">Avg Rating</div></div>', unsafe_allow_html=True)

with colC:
    st.markdown('<div class="metric-card"><div class="metric-value">'
                f'{df["reviews"].sum()}'
                '</div><div class="metric-label">Total Reviews</div></div>', unsafe_allow_html=True)

with colD:
    st.markdown('<div class="metric-card"><div class="metric-value">'
                f'{len(df)}'
                '</div><div class="metric-label">Total Products</div></div>', unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ----------------------------------------------------
# Function to display charts nicely
# ----------------------------------------------------
def show_chart(fig):
    st.pyplot(fig)
    st.markdown("<hr>", unsafe_allow_html=True)


# ----------------------------------------------------
# ANALYSIS BLOCKS
# ----------------------------------------------------

# ------------------- 1 — Average Price by Category
if menu == "Average Price by Category":
    st.markdown('<div class="section-header">💰 Average Price by Category</div>', unsafe_allow_html=True)

    result = df.groupby('price_category')['price'].mean().sort_values()

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Table View")
        st.dataframe(result, use_container_width=True)

    with col2:
        fig, ax = plt.subplots(figsize=(10, 6))
        result.plot(kind="bar", color="#3498db", ax=ax)
        ax.set_title("Average Price by Category")
        ax.set_xlabel("Category")
        ax.set_ylabel("Average Price")
        show_chart(fig)


# ------------------- 2 — Rating vs Price
elif menu == "Rating vs Price":
    st.markdown('<div class="section-header">⭐ Rating vs Price</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Sample Data")
        st.dataframe(df[['rating', 'price']].head(20), use_container_width=True)

    with col2:
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(df['rating'], df['price'], alpha=0.7, c="#8e44ad")
        ax.set_xlabel("Rating")
        ax.set_ylabel("Price")
        ax.set_title("Rating vs Price Scatter Plot")
        show_chart(fig)


# ------------------- 3 — Product Distribution by Category
elif menu == "Product Distribution by Category":
    st.markdown('<div class="section-header">📦 Product Distribution by Price Category</div>', unsafe_allow_html=True)

    counts = df['price_category'].value_counts()

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Category Counts")
        st.dataframe(counts, use_container_width=True)

    with col2:
        fig, ax = plt.subplots(figsize=(7, 7))
        counts.plot(kind="pie", autopct="%1.1f%%",
                    colors=["#1abc9c", "#3498db", "#e74c3c"],
                    ax=ax, startangle=90)
        ax.set_ylabel("")
        ax.set_title("Distribution of Products by Category")
        show_chart(fig)


# ------------------- 4 — Reviews vs Price
elif menu == "Reviews vs Price":
    st.markdown('<div class="section-header">📝 Reviews vs Price</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Sample Data")
        st.dataframe(df[['reviews', 'price']].head(20), use_container_width=True)

    with col2:
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(df['reviews'], df['price'], alpha=0.7, color="#e67e22")
        ax.set_xlabel("Number of Reviews")
        ax.set_ylabel("Price")
        ax.set_title("Reviews vs Price Scatter Plot")
        show_chart(fig)


# ------------------- 5 — Number of Products by Rating
elif menu == "Number of Products by Rating":
    st.markdown('<div class="section-header">📊 Number of Products by Rating</div>', unsafe_allow_html=True)

    counts = df['rating'].value_counts().sort_index()

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Ratings Table")
        st.dataframe(counts, use_container_width=True)

    with col2:
        fig, ax = plt.subplots(figsize=(10, 6))
        counts.plot(kind="bar", color="#9b59b6", ax=ax)
        ax.set_xlabel("Rating")
        ax.set_ylabel("Count")
        ax.set_title("Count of Products by Rating")
        show_chart(fig)
