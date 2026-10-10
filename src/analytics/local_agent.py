
from pathlib import Path

from metrics import (
    total_business_metrics,
    revenue_by_region,
    revenue_by_product,
    top_customers,
    monthly_revenue,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def format_currency(value):
    return f"₹{float(value or 0):,.2f}"


def answer_question(question):
    text = question.lower().strip()

    if any(word in text for word in [
        "region", "regional", "area"
    ]):
        rows = revenue_by_region()

        if not rows:
            return "No regional revenue data was found."

        best = rows[0]

        result = (
            f"The highest-revenue region is {best['region']}, "
            f"with revenue of "
            f"{format_currency(best['total_revenue'])}.\n\n"
            "Regional revenue breakdown:\n"
        )

        for row in rows:
            result += (
                f"- {row['region']}: "
                f"{format_currency(row['total_revenue'])}\n"
            )

        return result

    if "customer" in text:
        rows = top_customers(5)

        result = "Top 5 customers by revenue:\n"

        for index, row in enumerate(rows, start=1):
            result += (
                f"{index}. {row['customer_name']}: "
                f"{format_currency(row['total_revenue'])}\n"
            )

        return result

    if any(word in text for word in [
        "monthly", "month", "trend"
    ]):
        rows = monthly_revenue()

        result = "Monthly revenue:\n"

        for row in rows:
            result += (
                f"- {row['year_month']}: "
                f"{format_currency(row['total_revenue'])}\n"
            )

        return result

    if "product" in text:
        rows = revenue_by_product()

        if "top 3" in text or "three" in text:
            rows = rows[:3]
        elif "top 5" in text or "five" in text:
            rows = rows[:5]

        result = "Products ranked by revenue:\n"

        for index, row in enumerate(rows, start=1):
            result += (
                f"{index}. {row['product_name']}: "
                f"{format_currency(row['total_revenue'])}\n"
            )

        return result

    if any(word in text for word in [
        "overall", "total", "business performance",
        "profit", "how is the business"
    ]):
        metrics = total_business_metrics()

        return (
            "Overall business performance:\n"
            f"- Total orders: {metrics['total_orders']}\n"
            f"- Unique customers: {metrics['unique_customers']}\n"
            f"- Total revenue: "
            f"{format_currency(metrics['total_revenue'])}\n"
            f"- Total profit: "
            f"{format_currency(metrics['total_profit'])}"
        )

    return (
        "I couldn't identify the required analysis. "
        "Try asking about revenue by region, products, "
        "customers, monthly revenue, or total profit."
    )


def main():
    print("=" * 55)
    print("LOCAL BUSINESS INTELLIGENCE AGENT")
    print("No OpenAI API calls required")
    print("=" * 55)

    while True:
        question = input(
            "\nAsk a business question (or type 'exit'): "
        ).strip()

        if question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        if not question:
            continue

        try:
            print("\nBUSINESS ANSWER")
            print("-" * 55)
            print(answer_question(question))
        except Exception as error:
            print(f"Analysis failed: {error}")


if __name__ == "__main__":
    main()
