from io import BytesIO
import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import requests
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "src" / "analytics"))

from metrics import (
    total_business_metrics,
    revenue_by_region,
    revenue_by_product,
    top_customers,
    monthly_revenue,
    business_metrics_by_date,
)

API_URL = "http://127.0.0.1:8000/ask"

st.set_page_config(
    page_title="Enterprise BI Intelligence",
    page_icon="📊",
    layout="wide",
)

# Dashboard styling
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }
    [data-testid="stMetric"] {
        background: rgba(128, 128, 128, 0.08);
        border: 1px solid rgba(128, 128, 128, 0.2);
        padding: 16px;
        border-radius: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar
with st.sidebar:
    st.title("Enterprise BI")
    st.caption("Business Intelligence Platform")

    page = st.radio(
        "Navigation",
        ["Executive Overview", "AI Business Assistant"],
    )

    st.divider()
    st.caption("Data source: SQLite business database")
    st.caption("AI service: FastAPI + Google Gemini")

st.title("📊 Enterprise Business Intelligence")
st.caption(
    "Monitor revenue, profitability, customers, and business performance."
)

if page == "Executive Overview":
    try:
        st.subheader("Business Performance Date Filter")

        date_col1, date_col2 = st.columns(2)

        with date_col1:
            start_date = st.date_input(
                "Start date",
                value=pd.Timestamp("2026-01-01").date(),
                key="metrics_start_date",
            )

        with date_col2:
            end_date = st.date_input(
                "End date",
                value=pd.Timestamp("2026-12-31").date(),
                key="metrics_end_date",
            )

        if start_date > end_date:
            st.error("Start date cannot be after end date.")
            st.stop()

        # Date-filtered KPI metrics
        metrics = business_metrics_by_date(
            start_date.isoformat(),
            end_date.isoformat(),
        )

        # Existing analytics tables
        regions = pd.DataFrame(revenue_by_region())
        products = pd.DataFrame(revenue_by_product())
        customers = pd.DataFrame(top_customers(limit=5))
        monthly = pd.DataFrame(monthly_revenue())

        # Filter charts and tables to the selected date range.
        # The analytics functions above return aggregated results, so
        # date-specific chart data is queried directly from SQLite.
        from metrics import execute_query

        date_filter = """
            date(o.order_date) BETWEEN date(?) AND date(?)
        """
        date_params = (
            start_date.isoformat(),
            end_date.isoformat(),
        )

        regions = pd.DataFrame(
            execute_query(
                f"""
                SELECT
                    o.region,
                    SUM(
                        p.unit_price * o.quantity * (1 - o.discount)
                    ) AS total_revenue
                FROM orders o
                JOIN products p ON o.product_id = p.product_id
                WHERE {date_filter}
                GROUP BY o.region
                ORDER BY total_revenue DESC
                """,
                date_params,
            )
        )

        products = pd.DataFrame(
            execute_query(
                f"""
                SELECT
                    p.product_name,
                    SUM(
                        p.unit_price * o.quantity * (1 - o.discount)
                    ) AS total_revenue
                FROM orders o
                JOIN products p ON o.product_id = p.product_id
                WHERE {date_filter}
                GROUP BY p.product_id, p.product_name
                ORDER BY total_revenue DESC
                """,
                date_params,
            )
        )

        customers = pd.DataFrame(
            execute_query(
                f"""
                SELECT
                    c.customer_name,
                    SUM(
                        p.unit_price * o.quantity * (1 - o.discount)
                    ) AS total_revenue
                FROM orders o
                JOIN products p ON o.product_id = p.product_id
                JOIN customers c ON o.customer_id = c.customer_id
                WHERE {date_filter}
                GROUP BY c.customer_id, c.customer_name
                ORDER BY total_revenue DESC
                LIMIT 5
                """,
                date_params,
            )
        )

        monthly = pd.DataFrame(
            execute_query(
                f"""
                SELECT
                    strftime('%Y-%m', o.order_date) AS year_month,
                    SUM(
                        p.unit_price * o.quantity * (1 - o.discount)
                    ) AS total_revenue
                FROM orders o
                JOIN products p ON o.product_id = p.product_id
                WHERE {date_filter}
                GROUP BY year_month
                ORDER BY year_month
                """,
                date_params,
            )
        )

        st.caption(
            f"Showing data from {start_date.isoformat()} "
            f"to {end_date.isoformat()} (inclusive)."
        )

        # KPI cards
        revenue = metrics.get("total_revenue") or 0
        profit = metrics.get("total_profit") or 0
        orders = metrics.get("total_orders") or 0
        unique_customers = metrics.get("unique_customers") or 0
        margin = (profit / revenue * 100) if revenue else 0

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Revenue", f"₹{revenue:,.0f}")
        col2.metric("Total Profit", f"₹{profit:,.0f}")
        col3.metric("Profit Margin", f"{margin:.1f}%")

        col4, col5 = st.columns(2)
        col4.metric("Total Orders", f"{orders:,}")
        col5.metric("Unique Customers", f"{unique_customers:,}")

        st.divider()

        # Monthly revenue
        st.subheader("Monthly Revenue Trend")

        if not monthly.empty:
            fig_monthly = px.line(
                monthly,
                x="year_month",
                y="total_revenue",
                markers=True,
                labels={
                    "year_month": "Month",
                    "total_revenue": "Revenue (₹)",
                },
                title="Revenue by Month",
            )
            fig_monthly.update_layout(
                hovermode="x unified",
                yaxis_tickformat=",.0f",
            )
            st.plotly_chart(
                fig_monthly,
                use_container_width=True,
            )
        else:
            st.info("No monthly revenue data is available for this date range.")

        # Regional and product charts
        left, right = st.columns(2)

        with left:
            st.subheader("Revenue by Region")

            if not regions.empty:
                fig_region = px.bar(
                    regions,
                    x="region",
                    y="total_revenue",
                    labels={
                        "region": "Region",
                        "total_revenue": "Revenue (₹)",
                    },
                    title="Regional Performance",
                )
                fig_region.update_layout(yaxis_tickformat=",.0f")
                st.plotly_chart(
                    fig_region,
                    use_container_width=True,
                )
            else:
                st.info("No regional data is available for this date range.")

        with right:
            st.subheader("Revenue by Product")

            if not products.empty:
                fig_product = px.bar(
                    products.sort_values("total_revenue"),
                    x="total_revenue",
                    y="product_name",
                    orientation="h",
                    labels={
                        "product_name": "Product",
                        "total_revenue": "Revenue (₹)",
                    },
                    title="Product Performance",
                )
                fig_product.update_layout(xaxis_tickformat=",.0f")
                st.plotly_chart(
                    fig_product,
                    use_container_width=True,
                )
            else:
                st.info("No product data is available for this date range.")

        # Top customers
        st.subheader("Top 5 Customers by Revenue")

        if not customers.empty:
            customers_display = customers.rename(
                columns={
                    "customer_name": "Customer",
                    "total_revenue": "Revenue (₹)",
                }
            )
            st.dataframe(
                customers_display,
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No customer data is available for this date range.")
        
        # Top 5 Customers
        st.subheader("Top 5 Customers by Revenue")

        if not customers.empty:
            customers_display = customers.rename(
                columns={
                    "customer_name": "Customer",
                    "total_revenue": "Revenue (₹)",
                }
            )
            st.dataframe(
                customers_display,
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No customer data is available for this date range.")

        # PASTE THE COMPLETE REPORT DOWNLOAD CODE HERE

        with st.expander("View underlying analytics data"):
            st.write("Regional revenue")
            # Keep the existing code below unchanged


        with st.expander("View underlying analytics data"):
            st.write("Regional revenue")
            st.dataframe(
                regions,
                use_container_width=True,
                hide_index=True,
            )

            st.write("Product revenue")
            st.dataframe(
                products,
                use_container_width=True,
                hide_index=True,
            )

            st.write("Monthly revenue")
            st.dataframe(
                monthly,
                use_container_width=True,
                hide_index=True,
            )

    except Exception as error:
        st.error(f"Could not load business analytics: {error}")
        st.info(
            "Check that data/business.db exists and that the database "
            "has been created successfully."
        )

else:
    st.subheader("🤖 AI Business Assistant")
    st.write(
        "Ask questions about business metrics, customers, regional "
        "performance, or company policies."
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()

    question = st.chat_input("Ask a business question...")

    if question:
        st.session_state.messages.append(
            {"role": "user", "content": question}
        )

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing your question..."):
                try:
                    response = requests.post(
                        API_URL,
                        json={"question": question},
                        timeout=120,
                    )
                    response.raise_for_status()

                    answer = response.json().get(
                        "answer",
                        "No answer returned.",
                    )

                except requests.exceptions.Timeout:
                    answer = "The request timed out. Please try again."

                except requests.exceptions.ConnectionError:
                    answer = (
                        "Cannot connect to FastAPI. Ensure the backend "
                        "is running at http://127.0.0.1:8000."
                    )

                except requests.exceptions.HTTPError as error:
                    try:
                        answer = str(
                            response.json().get("detail", str(error))
                        )
                    except ValueError:
                        answer = str(error)

                except requests.exceptions.RequestException as error:
                    answer = f"Request failed: {error}"

                st.markdown(answer)

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )
