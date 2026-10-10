
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src" / "analytics"))

from metrics import (
    total_business_metrics,
    revenue_by_region,
    revenue_by_product,
    top_customers,
    monthly_revenue,
)


def test_total_business_metrics():
    result = total_business_metrics()

    assert result["total_orders"] > 0
    assert result["unique_customers"] > 0
    assert result["total_revenue"] > 0
    assert result["total_profit"] > 0


def test_revenue_by_region():
    results = revenue_by_region()

    assert len(results) > 0
    assert all(row["total_revenue"] >= 0 for row in results)
    assert results == sorted(
        results,
        key=lambda row: row["total_revenue"],
        reverse=True,
    )


def test_revenue_by_product():
    results = revenue_by_product()

    assert len(results) > 0
    assert all(row["product_name"] for row in results)
    assert all(row["total_revenue"] >= 0 for row in results)


def test_top_customers():
    results = top_customers(limit=5)

    assert len(results) == 5
    assert results == sorted(
        results,
        key=lambda row: row["total_revenue"],
        reverse=True,
    )


def test_monthly_revenue():
    results = monthly_revenue()

    assert len(results) > 0
    assert all(row["year_month"] for row in results)
    assert all(row["total_revenue"] >= 0 for row in results)
