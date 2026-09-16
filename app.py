import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="AI Sales Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================
st.markdown("""
<style>

.main {
    background-color: #f7f9fc;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}

/* Main title */
.hero-title {
    font-size: 38px;
    font-weight: 800;
    margin-bottom: 5px;
}

.hero-subtitle {
    font-size: 17px;
    color: #667085;
    margin-bottom: 25px;
}

/* KPI Cards */
.kpi-card {
    background: white;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #e6eaf0;
    box-shadow: 0 3px 12px rgba(0,0,0,0.05);
    min-height: 125px;
}

.kpi-label {
    color: #667085;
    font-size: 14px;
    font-weight: 600;
}

.kpi-value {
    font-size: 28px;
    font-weight: 800;
    margin-top: 8px;
}

/* Section */
.section-title {
    font-size: 24px;
    font-weight: 750;
    margin-top: 20px;
    margin-bottom: 15px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

/* Assistant */
.assistant-box {
    background: white;
    padding: 25px;
    border-radius: 15px;
    border: 1px solid #e6eaf0;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD DATA
# =========================================================
@st.cache_data
def load_data():
    data = pd.read_csv("data/sales.csv")
    data["Order_Date"] = pd.to_datetime(data["Order_Date"])
    return data


df = load_data()

# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.markdown("## 📊 Sales Intelligence")
st.sidebar.markdown("---")

st.sidebar.markdown("### Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "🏠 Overview",
        "📈 Sales Analysis",
        "👥 Customer Segmentation",
        "🔮 Sales Forecast",
        "🤖 AI Assistant"
    ],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")



# =========================================================
# HEADER
# =========================================================
st.markdown(
    '<div class="hero-title">🤖 AI-Powered Sales & Customer Intelligence</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-subtitle">'
    'Analyze sales performance, understand customers and forecast future trends.'
    '</div>',
    unsafe_allow_html=True
)

# =========================================================
# FILTER BAR
# =========================================================
st.markdown("### 🔎 Filters")

filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)

with filter_col1:
    date_range = st.date_input(
        "📅 Date Range",
        value=(
            df["Order_Date"].min().date(),
            df["Order_Date"].max().date()
        ),
        min_value=df["Order_Date"].min().date(),
        max_value=df["Order_Date"].max().date()
    )

with filter_col2:
    region = st.selectbox(
        "🌍 Region",
        ["All Regions"] + sorted(df["Region"].unique())
    )

with filter_col3:
    category = st.selectbox(
        "📦 Category",
        ["All Categories"] + sorted(df["Category"].unique())
    )

with filter_col4:
    product = st.selectbox(
        "🛒 Product",
        ["All Products"] + sorted(df["Product"].unique())
    )


# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = df.copy()

if len(date_range) == 2:
    start_date, end_date = date_range

    filtered_df = filtered_df[
        (filtered_df["Order_Date"].dt.date >= start_date) &
        (filtered_df["Order_Date"].dt.date <= end_date)
    ]

if region != "All Regions":
    filtered_df = filtered_df[
        filtered_df["Region"] == region
    ]

if category != "All Categories":
    filtered_df = filtered_df[
        filtered_df["Category"] == category
    ]

if product != "All Products":
    filtered_df = filtered_df[
        filtered_df["Product"] == product
    ]

st.markdown("---")

# =========================================================
# KPI CALCULATIONS
# =========================================================
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order_ID"].nunique()
total_customers = filtered_df["Customer_ID"].nunique()

profit_margin = (
    total_profit / total_sales * 100
    if total_sales > 0 else 0
)

# =========================================================
# OVERVIEW
# =========================================================
if page == "🏠 Overview":

    st.markdown(
        '<div class="section-title">📌 Business Overview</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3, c4, c5 = st.columns(5)

    cards = [
        ("Total Sales", f"₹{total_sales/1e7:.2f} Cr"),
        ("Total Profit", f"₹{total_profit/1e7:.2f} Cr"),
        ("Orders", f"{total_orders:,}"),
        ("Customers", f"{total_customers:,}"),
        ("Profit Margin", f"{profit_margin:.2f}%")
    ]

    for col, (label, value) in zip(
        [c1, c2, c3, c4, c5],
        cards
    ):
        with col:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-label">{label}</div>
                    <div class="kpi-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.write("")

    # Monthly trend
    monthly = (
        filtered_df
        .groupby(filtered_df["Order_Date"].dt.to_period("M"))["Sales"]
        .sum()
        .reset_index()
    )

    monthly["Order_Date"] = monthly["Order_Date"].dt.to_timestamp()

    fig_monthly = px.line(
        monthly,
        x="Order_Date",
        y="Sales",
        markers=True,
        title="Monthly Sales Trend"
    )

    fig_monthly.update_layout(
        template="plotly_white",
        height=420,
        xaxis_title="Month",
        yaxis_title="Sales"
    )

    st.plotly_chart(
        fig_monthly,
        use_container_width=True
    )

    # Category + Region
    c1, c2 = st.columns(2)

    category_sales = (
        filtered_df
        .groupby("Category")["Sales"]
        .sum()
        .reset_index()
        .sort_values("Sales", ascending=False)
    )

    fig_category = px.bar(
        category_sales,
        x="Sales",
        y="Category",
        orientation="h",
        title="Sales by Category"
    )

    fig_category.update_layout(
        template="plotly_white",
        height=380
    )

    c1.plotly_chart(
        fig_category,
        use_container_width=True
    )

    region_sales = (
        filtered_df
        .groupby("Region")["Sales"]
        .sum()
        .reset_index()
        .sort_values("Sales", ascending=False)
    )

    fig_region = px.bar(
        region_sales,
        x="Sales",
        y="Region",
        orientation="h",
        title="Sales by Region"
    )

    fig_region.update_layout(
        template="plotly_white",
        height=380
    )

    c2.plotly_chart(
        fig_region,
        use_container_width=True
    )

# =========================================================
# SALES ANALYSIS
# =========================================================
elif page == "📈 Sales Analysis":

    st.markdown(
        '<div class="section-title">📈 Sales Performance Analysis</div>',
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    # Top Products
    product_sales = (
        filtered_df
        .groupby("Product")["Sales"]
        .sum()
        .reset_index()
        .sort_values("Sales", ascending=False)
        .head(10)
    )

    fig_product = px.bar(
        product_sales,
        x="Sales",
        y="Product",
        orientation="h",
        title="Top 10 Products by Sales"
    )

    fig_product.update_layout(
        template="plotly_white",
        height=500
    )

    c1.plotly_chart(
        fig_product,
        use_container_width=True
    )

    # Sales vs Profit
    fig_scatter = px.scatter(
        filtered_df,
        x="Sales",
        y="Profit",
        title="Sales vs Profit",
        hover_data=["Product", "Category", "Region"]
    )

    fig_scatter.update_layout(
        template="plotly_white",
        height=500
    )

    c2.plotly_chart(
        fig_scatter,
        use_container_width=True
    )

    st.subheader("📋 Category Profitability")

    category_profit = (
        filtered_df
        .groupby("Category")
        .agg(
            Total_Sales=("Sales", "sum"),
            Total_Profit=("Profit", "sum")
        )
        .reset_index()
    )

    category_profit["Profit_Margin"] = (
        category_profit["Total_Profit"] /
        category_profit["Total_Sales"] * 100
    ).round(2)

    st.dataframe(
        category_profit,
        use_container_width=True,
        hide_index=True
    )

# =========================================================
# CUSTOMER SEGMENTATION
# =========================================================
elif page == "👥 Customer Segmentation":

    st.markdown(
        '<div class="section-title">👥 Customer Segmentation</div>',
        unsafe_allow_html=True
    )

    reference_date = (
        df["Order_Date"].max() +
        pd.Timedelta(days=1)
    )

    rfm = df.groupby("Customer_ID").agg(
        Recency=(
            "Order_Date",
            lambda x: (reference_date - x.max()).days
        ),
        Frequency=("Order_ID", "nunique"),
        Monetary=("Sales", "sum")
    ).reset_index()

    features = [
        "Recency",
        "Frequency",
        "Monetary"
    ]

    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(
        rfm[features]
    )

    kmeans = KMeans(
        n_clusters=3,
        random_state=42,
        n_init=10
    )

    rfm["Cluster"] = kmeans.fit_predict(
        X_scaled
    )

    c1, c2 = st.columns([1, 2])

    with c1:

        st.subheader("Segment Summary")

        summary = (
            rfm
            .groupby("Cluster")[features]
            .mean()
            .round(2)
        )

        st.dataframe(
            summary,
            use_container_width=True
        )

        st.metric(
            "Total Customers",
            len(rfm)
        )

    with c2:

        fig_clusters = px.scatter(
            rfm,
            x="Frequency",
            y="Monetary",
            color=rfm["Cluster"].astype(str),
            hover_data=[
                "Customer_ID",
                "Recency"
            ],
            title="Customer Segments"
        )

        fig_clusters.update_layout(
            template="plotly_white",
            height=500
        )

        st.plotly_chart(
            fig_clusters,
            use_container_width=True
        )

    st.info(
        "K-Means groups customers based on Recency, Frequency and Monetary value."
    )

# =========================================================
# FORECAST
# =========================================================
elif page == "🔮 Sales Forecast":

    st.markdown(
        '<div class="section-title">🔮 Sales Forecasting</div>',
        unsafe_allow_html=True
    )

    forecast = (
        df
        .groupby(df["Order_Date"].dt.to_period("M"))["Sales"]
        .sum()
        .reset_index()
    )

    forecast["Order_Date"] = (
        forecast["Order_Date"].dt.to_timestamp()
    )

    forecast["Month_Number"] = range(
        1,
        len(forecast) + 1
    )

    X = forecast[["Month_Number"]]
    y = forecast["Sales"]

    model = LinearRegression()

    model.fit(X, y)

    forecast["Predicted_Sales"] = (
        model.predict(X)
    )

    fig = px.line(
        forecast,
        x="Order_Date",
        y=[
            "Sales",
            "Predicted_Sales"
        ],
        markers=True,
        title="Actual vs Predicted Sales"
    )

    fig.update_layout(
        template="plotly_white",
        height=500,
        xaxis_title="Month",
        yaxis_title="Sales"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.info(
        "Linear Regression is used as a simple baseline model "
        "to identify the overall sales trend."
    )

# =========================================================
# AI ASSISTANT
# =========================================================
elif page == "🤖 AI Assistant":

    st.markdown(
        '<div class="section-title">🤖 Business Intelligence Assistant</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="assistant-box">
        Ask questions about your sales data and get instant business insights.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    question = st.text_input(
        "💬 Ask your question",
        placeholder="Example: What is the total sales?"
    )

    if question:

        q = question.lower()

        if "total sales" in q:

            st.success(
                f"💰 Total Sales: ₹{df['Sales'].sum():,.2f}"
            )

        elif "total profit" in q:

            st.success(
                f"💵 Total Profit: ₹{df['Profit'].sum():,.2f}"
            )

        elif "top product" in q:

            top_product = (
                df.groupby("Product")["Sales"]
                .sum()
                .idxmax()
            )

            st.success(
                f"🏆 Top Product by Sales: {top_product}"
            )

        elif "top region" in q:

            top_region = (
                df.groupby("Region")["Sales"]
                .sum()
                .idxmax()
            )

            st.success(
                f"🌍 Top Region by Sales: {top_region}"
            )

        elif "profit margin" in q:

            margin = (
                df["Profit"].sum() /
                df["Sales"].sum()
                * 100
            )

            st.success(
                f"📊 Overall Profit Margin: {margin:.2f}%"
            )

        else:

            st.warning(
                "Try asking: total sales, total profit, "
                "top product, top region or profit margin."
            )

# =========================================================
# FOOTER
# =========================================================
st.markdown("---")

st.caption(
    "AI-Powered Sales & Customer Intelligence System  •  "
    "Python • Pandas • SQL • Power BI • Scikit-learn • Streamlit"
)