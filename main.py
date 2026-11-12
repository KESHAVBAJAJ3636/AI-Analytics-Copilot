
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path

print("======================================")
print("          AI ANALYTICS COPILOT")
print("======================================")

file_path = Path(__file__).parent / "sample_data.csv"

try:
    # Load dataset
    data = pd.read_csv(file_path)

    print("\nDATA LOADED SUCCESSFULLY!")

    # Calculate business metrics
    total_sales = data["Sales"].sum()
    total_profit = data["Profit"].sum()
    total_quantity = data["Quantity"].sum()

    print("\n========== BUSINESS SUMMARY ==========")
    print("Total Sales: Rs.", total_sales)
    print("Total Profit: Rs.", total_profit)
    print("Total Quantity Sold:", total_quantity)

    # Region-wise analysis
    region_sales = (
        data.groupby("Region")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    # Product-wise analysis
    product_summary = (
        data.groupby("Product")[["Sales", "Profit"]]
        .sum()
        .reset_index()
    )

    print("\n========== REGION-WISE SALES ==========")
    print(region_sales)

    print("\n========== PRODUCT-WISE ANALYSIS ==========")
    print(product_summary.to_string(index=False))

    # Create dashboard with three charts
    fig = make_subplots(
        rows=1,
        cols=3,
        subplot_titles=(
            "Region-wise Sales",
            "Product-wise Sales",
            "Sales vs Profit"
        )
    )

    # Chart 1: Region-wise Sales
    fig.add_trace(
        go.Bar(
            x=region_sales.index,
            y=region_sales.values,
            name="Regional Sales"
        ),
        row=1,
        col=1
    )

    # Chart 2: Product-wise Sales
    fig.add_trace(
        go.Bar(
            x=product_summary["Product"],
            y=product_summary["Sales"],
            name="Product Sales"
        ),
        row=1,
        col=2
    )

    # Chart 3: Sales vs Profit
    fig.add_trace(
        go.Bar(
            x=product_summary["Product"],
            y=product_summary["Sales"],
            name="Sales"
        ),
        row=1,
        col=3
    )

    fig.add_trace(
        go.Bar(
            x=product_summary["Product"],
            y=product_summary["Profit"],
            name="Profit"
        ),
        row=1,
        col=3
    )

    # Dashboard layout
    fig.update_layout(
        title="AI Analytics Copilot - Business Dashboard",
        height=600,
        width=1500,
        barmode="group",
        template="plotly_white"
    )

    # Add axis labels
    fig.update_xaxes(title_text="Region", row=1, col=1)
    fig.update_xaxes(title_text="Product", row=1, col=2)
    fig.update_xaxes(title_text="Product", row=1, col=3)

    fig.update_yaxes(title_text="Sales (Rs.)", row=1, col=1)
    fig.update_yaxes(title_text="Sales (Rs.)", row=1, col=2)
    fig.update_yaxes(title_text="Amount (Rs.)", row=1, col=3)

    # Save and open dashboard
    dashboard_path = Path(__file__).parent / "dashboard.html"

    fig.write_html(
        dashboard_path,
        include_plotlyjs=True,
        auto_open=True
    )

    print("\n======================================")
    print("DASHBOARD CREATED SUCCESSFULLY!")
    print("Dashboard File:", dashboard_path)
    print("======================================")

except FileNotFoundError:
    print("\nERROR: sample_data.csv file not found.")

except KeyError as error:
    print("\nERROR: Required column is missing:", error)

except Exception as error:
    print("\nSomething went wrong:", error)
