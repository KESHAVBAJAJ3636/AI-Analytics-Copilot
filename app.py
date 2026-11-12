
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from sklearn.ensemble import IsolationForest
# Page configuration
st.set_page_config(
    page_title="AI Analytics Copilot",
    page_icon="📊",
    layout="wide"
)

# Professional Dashboard Styling
st.markdown("""
<style>
    /* Main Dashboard Background */
    [data-testid="stAppViewContainer"] {
        background-color: #F5F7FB;
    }

    [data-testid="stHeader"] {
        background-color: #F5F7FB;
    }

    /* Main Content */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Main Heading */
    h1 {
        color: #17365D;
        font-weight: 700;
    }

    h2, h3 {
        color: #24476B;
        font-weight: 600;
    }

    /* KPI Metric Cards */
    [data-testid="stMetric"] {
        background-color: white;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #EDF2F8;
    }

    /* Buttons */
    .stButton button {
        background-color: #17365D;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 8px 18px;
    }

    .stButton button:hover {
        background-color: #24476B;
        color: white;
    }

    /* Data Tables */
    [data-testid="stDataFrame"] {
        border: 1px solid #E2E8F0;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Application title
st.title("📊 AI Analytics Copilot")
st.write("Interactive Business Analytics Dashboard")

# Load dataset
st.sidebar.header("Upload Business Data")
st.sidebar.markdown("---")
st.sidebar.subheader("📁 Data Management")

st.sidebar.caption(
    "Upload your business dataset in CSV or Excel format."
)
uploaded_file = st.sidebar.file_uploader(
    "Upload CSV or Excel file",
    type=["csv", "xlsx"]
)

try:
    if uploaded_file is not None:
        if uploaded_file.name.endswith(".csv"):
            data = pd.read_csv(uploaded_file)
        else:
            data = pd.read_excel(uploaded_file)
    else:
        file_path = Path(__file__).parent / "sample_data.csv"
        data = pd.read_csv(file_path)

    # Validate required columns
    required_columns = [
        "Date", "Region", "Product",
        "Sales", "Profit", "Quantity", "Customer"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in data.columns
    ]

    if missing_columns:
        st.error("Missing required columns: " + ", ".join(missing_columns))
        st.stop()

    # Convert numeric columns
    data["Sales"] = pd.to_numeric(data["Sales"], errors="coerce")
    data["Profit"] = pd.to_numeric(data["Profit"], errors="coerce")
    data["Quantity"] = pd.to_numeric(data["Quantity"], errors="coerce")

    # Remove rows with missing required numeric values
    data = data.dropna(subset=["Sales", "Profit", "Quantity"])

    if data.empty:
        st.error("No valid business records found in the dataset.")
        st.stop()




    # Anomaly Detection
    if len(data) >= 10:
        anomaly_model = IsolationForest(
            n_estimators=100,
            contamination="auto",
            random_state=42
        )

        data["Anomaly"] = anomaly_model.fit_predict(
            data[["Sales", "Profit", "Quantity"]]
        )

        data["Anomaly Status"] = data["Anomaly"].map({
            1: "Normal",
            -1: "Anomaly"
        })
    else:
        data["Anomaly"] = 1
        data["Anomaly Status"] = "Normal"
       # Dashboard Filters
    st.sidebar.divider()
    st.sidebar.header("Dashboard Filters")




    st.sidebar.markdown("---")
    st.sidebar.subheader("📁 Data Management")

    st.sidebar.caption(
        "Upload your business dataset in CSV or Excel format."
    )
    data["Region"] = data["Region"].astype(str)
    data["Product"] = data["Product"].astype(str)

    regions = ["All"] + sorted(data["Region"].unique().tolist())
    products = ["All"] + sorted(data["Product"].unique().tolist())

    selected_region = st.sidebar.selectbox(
        "Select Region",
        regions
    )

    selected_product = st.sidebar.selectbox(
        "Select Product",
        products
    )

    if selected_region != "All":
        data = data[data["Region"] == selected_region]

    if selected_product != "All":
        data = data[data["Product"] == selected_product]

    if data.empty:
        st.warning("No records found for selected filters.")
        st.stop()
    # Calculate business metrics
    total_sales = data["Sales"].sum()
    total_profit = data["Profit"].sum()
    total_quantity = data["Quantity"].sum()
    average_sales = data["Sales"].mean()

    # KPI metrics
    st.subheader("Business Performance Overview")

    # Professional KPI Cards
    st.subheader("Business Performance Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="💰 Total Sales",
            value=f"₹{total_sales:,.0f}",
            help="Total revenue generated"
        )

    with col2:
        st.metric(
            label="📈 Total Profit",
            value=f"₹{total_profit:,.0f}",
            help="Total profit generated"
        )

    with col3:
        st.metric(
            label="📦 Quantity Sold",
            value=f"{total_quantity:,.0f}",
            help="Total units sold"
        )

    with col4:
        st.metric(
            label="📊 Average Sales",
            value=f"₹{average_sales:,.2f}",
            help="Average sales per record"
        )


    st.divider()


    # Region-wise sales
    st.subheader("Region-wise Sales Analysis")

    region_sales = (
        data.groupby("Region", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
    )

    region_chart = px.bar(
        region_sales,
        x="Region",
        y="Sales",
        color="Region",
        title="Regional Sales Performance",
        text_auto=True,
        template="plotly_white"
    )

    region_chart.update_layout(
        title_x=0.5,
        title_font_size=20,
        xaxis_title="Business Region",
        yaxis_title="Total Sales (₹)",
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=30, r=30, t=60, b=30)
    )

    region_chart.update_traces(
        textposition="outside",
        marker_line_width=1
    )

    st.plotly_chart(region_chart, use_container_width=True)


    
    # Product-wise sales
    st.subheader("Product-wise Sales Analysis")

    product_sales = (
        data.groupby("Product", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
    )

    product_chart = px.bar(
        product_sales,
        x="Product",
        y="Sales",
        color="Product",
        title="Product Sales Performance",
        text_auto=True,
        template="plotly_white"
    )

    product_chart.update_layout(
        title_x=0.5,
        title_font_size=20,
        xaxis_title="Business Product",
        yaxis_title="Total Sales (₹)",
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=30, r=30, t=60, b=30)
    )

    product_chart.update_traces(
        textposition="outside",
        marker_line_width=1
    )

    st.plotly_chart(product_chart, use_container_width=True)


   
    # Sales vs Profit
    st.subheader("Sales vs Profit Analysis")

    product_summary = (
        data.groupby("Product", as_index=False)[["Sales", "Profit"]]
        .sum()
    )

    comparison_data = product_summary.melt(
        id_vars="Product",
        value_vars=["Sales", "Profit"],
        var_name="Metric",
        value_name="Amount"
    )

    comparison_chart = px.bar(
        comparison_data,
        x="Product",
        y="Amount",
        color="Metric",
        barmode="group",
        title="Sales vs Profit by Product",
        text_auto=True,
        template="plotly_white"
    )

    comparison_chart.update_layout(
        title_x=0.5,
        title_font_size=20,
        xaxis_title="Business Product",
        yaxis_title="Amount (₹)",
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=30, r=30, t=60, b=30),
        legend_title_text="Business Metrics"
    )

    comparison_chart.update_traces(
        textposition="outside",
        marker_line_width=1
    )

    st.plotly_chart(comparison_chart, use_container_width=True)

    # Ask Your Data
    st.subheader("Ask Your Data")

    user_question = st.text_input(
        "Ask a question about your business data:",
        placeholder="Example: Which product has the highest sales?"
    )

    if st.button("Get Answer"):
        question = user_question.lower()

        if "total sales" in question:
            st.info(f"Total Sales: ₹{data['Sales'].sum():,.2f}")

        elif "total profit" in question:
            st.info(f"Total Profit: ₹{data['Profit'].sum():,.2f}")

        elif "average sales" in question:
            st.info(f"Average Sales: ₹{data['Sales'].mean():,.2f}")

        elif (
    "best product" in question
    or "highest sales product" in question
    or "product has the highest sales" in question
    or "which product sells the most" in question
):
            best_product = data.groupby("Product")["Sales"].sum().idxmax()
            st.success(f"Best Product: {best_product}")

        
        elif (
            "best region" in question
            or "highest sales region" in question
            or "which region has the highest sales" in question
            or "region has the highest sales" in question
            or "top region" in question
        ):
            best_region = data.groupby("Region")["Sales"].sum().idxmax()
            st.success(f"Best Region: {best_region}")


        elif "total records" in question:
            st.info(f"Total Records: {len(data)}")

        else:
            st.warning("Sorry, I cannot answer this question yet.")
       
    # Sales Trend Analysis
    st.subheader("Monthly Sales Trend Analysis")

    data["Date"] = pd.to_datetime(data["Date"], errors="coerce")

    
    # Sales Trend Analysis
    st.subheader("Monthly Sales Trend Analysis")

    data["Date"] = pd.to_datetime(data["Date"], errors="coerce")

    trend_data = (
        data.dropna(subset=["Date"])
        .groupby(data.dropna(subset=["Date"])["Date"].dt.to_period("M"))["Sales"]
        .sum()
        .reset_index()
    )

    trend_data["Date"] = trend_data["Date"].astype(str)

    if not trend_data.empty:
        trend_chart = px.line(
            trend_data,
            x="Date",
            y="Sales",
            markers=True,
            title="Monthly Business Sales Trend",
            template="plotly_white"
        )

        trend_chart.update_layout(
            title_x=0.5,
            title_font_size=20,
            xaxis_title="Month",
            yaxis_title="Total Sales (₹)",
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(l=30, r=30, t=60, b=30)
        )

        trend_chart.update_traces(
            mode="lines+markers",
            line=dict(width=3),
            marker=dict(size=9)
        )

        st.plotly_chart(trend_chart, use_container_width=True)
    else:
        st.warning("No valid date data available for sales trend.")

    
    # Profitability Analysis
    st.subheader("Product-wise Profitability Analysis")

    profit_data = (
        data.groupby("Product", as_index=False)["Profit"]
        .sum()
        .sort_values("Profit", ascending=False)
    )

    profit_chart = px.bar(
        profit_data,
        x="Product",
        y="Profit",
        color="Product",
        title="Product Profitability Performance",
        text_auto=True,
        template="plotly_white"
    )

    profit_chart.update_layout(
        title_x=0.5,
        title_font_size=20,
        xaxis_title="Business Product",
        yaxis_title="Total Profit (₹)",
        showlegend=False,
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=30, r=30, t=60, b=30)
    )

    profit_chart.update_traces(
        textposition="outside",
        marker_line_width=1
    )

    st.plotly_chart(profit_chart, use_container_width=True)

    if not profit_data.empty:
        top_profit_product = profit_data.iloc[0]["Product"]
        st.success(
            f"Most profitable product: {top_profit_product}"
        )


    if not profit_data.empty:
        top_profit_product = profit_data.iloc[0]["Product"]
        st.success(
            f"Most profitable product: {top_profit_product}"
        )
         
    # Business Recommendations
    st.subheader("💡 Business Recommendations")

    region_performance = (
        data.groupby("Region")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    product_profitability = (
        data.groupby("Product")["Profit"]
        .sum()
        .sort_values(ascending=False)
    )

    recommendation_col1, recommendation_col2 = st.columns(2)

    if not region_performance.empty:
        best_region = region_performance.idxmax()
        low_region = region_performance.idxmin()

        with recommendation_col1:
            st.success(
                f"🏆 Top Performing Region: {best_region}"
            )
            st.info(
                f"📊 Review Region: {low_region} has the lowest sales."
            )

    if not product_profitability.empty:
        best_product = product_profitability.idxmax()
        low_product = product_profitability.idxmin()

        with recommendation_col2:
            st.success(
                f"💰 Most Profitable Product: {best_product}"
            )
            st.warning(
                f"⚠️ Review Product: {low_product} has the lowest profit."
            )

    # Business insights
    st.subheader("Automated Business Insights")

    best_region = region_sales.iloc[0]["Region"]
    best_product = product_sales.iloc[0]["Product"]

    st.success(f"Best performing region: {best_region}")
    st.success(f"Best selling product: {best_product}")


    # Dataset preview
    st.subheader("Dataset Preview")
    st.dataframe(data, use_container_width=True)
    # Anomaly Detection Report
    st.subheader("AI-Assisted Anomaly Detection")

    anomalies = data[data["Anomaly"] == -1]

    anomaly_col1, anomaly_col2 = st.columns(2)

    anomaly_col1.metric("Total Anomalies", len(anomalies))
    anomaly_col2.metric(
        "Normal Records",
        len(data) - len(anomalies)
    )

    if not anomalies.empty:
        st.warning("Unusual business transactions detected.")
        st.dataframe(
            anomalies,
            use_container_width=True
        )
    else:
        st.success("No unusual transactions detected.")
    # Data quality report
    st.subheader("Data Quality Report")

    quality_col1, quality_col2 = st.columns(2)

    quality_col1.metric("Total Records", len(data))
    quality_col2.metric(
        "Duplicate Records",
        int(data.duplicated().sum())
    )

    st.write("Missing values by column:")
    st.dataframe(
        data.isnull().sum().rename("Missing Values"),
        use_container_width=True
    )

except FileNotFoundError:
    st.error("sample_data.csv was not found in the project folder.")

except Exception as error:
    st.error(f"Something went wrong: {error}")
