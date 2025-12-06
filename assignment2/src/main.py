import sys
import os
import subprocess
from csv_loader import CSVLoader
from sales_analytics import SalesAnalytics


def print_header(title):
    """Prints a formatted section header."""
    print()
    print(title)
    print()


def format_currency(amount):
    """Formats a numeric value as currency."""
    return f"${amount:,.2f}"


def format_percent(value):
    """Formats a numeric value as a percentage."""
    return f"{value:.2f}%"


def main():
    """Runs the full sales analysis pipeline and executes unit tests."""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    analysis_path = os.path.join(project_root, "analysis.txt")

    analysis_file = open(analysis_path, "w")
    original_stdout = sys.stdout
    sys.stdout = analysis_file

    data_path = os.path.join('data', 'sales_data.csv')

    if not os.path.exists(data_path):
        sys.stdout = original_stdout
        analysis_file.close()
        print(f"Error: Data file not found at {data_path}")
        sys.exit(1)

    print("Loading sales data...")
    records = CSVLoader.load_sales_data(data_path)
    print(f"Successfully loaded {len(records)} transactions")

    analytics = SalesAnalytics(records)

    print_header("EXECUTIVE SUMMARY: STATISTICAL OVERVIEW")

    stats = analytics.summary_statistics()

    print("Sales Metrics:")
    print(f"  Total Revenue: {format_currency(stats['sales']['total'])}")
    print(f"  Average Transaction: {format_currency(stats['sales']['mean'])}")
    print(f"  Median Transaction: {format_currency(stats['sales']['median'])}")
    print(f"  Std Deviation: {format_currency(stats['sales']['std_dev'])}")
    print(f"  Range: {format_currency(stats['sales']['min'])} - {format_currency(stats['sales']['max'])}")

    print("\nProfitability Metrics:")
    print(f"  Total Profit: {format_currency(stats['profit']['total'])}")
    print(f"  Average Profit: {format_currency(stats['profit']['mean'])}")
    print(f"  Median Profit: {format_currency(stats['profit']['median'])}")
    print(f"  Std Deviation: {format_currency(stats['profit']['std_dev'])}")

    print("\nDiscount Metrics:")
    print(f"  Average Discount: {format_percent(stats['discount']['mean'] * 100)}")
    print(f"  Median Discount: {format_percent(stats['discount']['median'] * 100)}")
    print(f"  Range: {format_percent(stats['discount']['min'] * 100)} - {format_percent(stats['discount']['max'] * 100)}")

    print("\nProfit Margin:")
    print(f"  Average: {format_percent(stats['profit_margin']['mean'])}")
    print(f"  Median: {format_percent(stats['profit_margin']['median'])}")

    print_header("CATEGORY PERFORMANCE MATRIX")

    categories = analytics.category_performance_matrix()
    print(f"{'Category':<20} {'Total Sales':>13} {'Total Profit':>13} {'Margin':>8} {'Transactions':>13}")
    for category, metrics in categories.items():
        print(f"{category:<20} {format_currency(metrics['total_sales']):>13} "
              f"{format_currency(metrics['total_profit']):>13} {format_percent(metrics['profit_margin']):>8} "
              f"{metrics['transaction_count']:>13}")

    print_header("REGIONAL EFFICIENCY ANALYSIS")

    regions = analytics.regional_efficiency_analysis()
    print(f"{'Region':<15} {'Sales':>13} {'Profit':>13} {'Margin':>8} {'Cities':>8} {'Customers':>10}")
    for region, metrics in regions.items():
        print(f"{region:<15} {format_currency(metrics['total_sales']):>13} "
              f"{format_currency(metrics['total_profit']):>13} {format_percent(metrics['profit_margin']):>8} "
              f"{metrics['cities_served']:>8} {metrics['unique_customers']:>10}")

    print_header("DISCOUNT OPTIMIZATION ANALYSIS")

    discounts = analytics.discount_optimization_analysis()
    print(f"{'Bracket':<12} {'Transactions':>13} {'Total Sales':>13} {'Total Profit':>13} {'Margin':>8}")
    for bracket, metrics in discounts.items():
        print(f"{bracket:<12} {metrics['transaction_count']:>13} "
              f"{format_currency(metrics['total_sales']):>13} "
              f"{format_currency(metrics['total_profit']):>13} "
              f"{format_percent(metrics['profit_margin']):>8}")

    print_header("CUSTOMER SEGMENTATION ANALYSIS")

    segments = analytics.customer_segmentation_analysis()
    print(f"{'Segment':<15} {'Customers':>10} {'Total Sales':>13} {'Total Profit':>13} {'Avg per Customer':>17}")
    for name in ['high_value', 'medium_value', 'low_value']:
        s = segments[name]
        print(f"{name.replace('_', ' ').title():<15} {s['customer_count']:>10} "
              f"{format_currency(s['total_sales']):>13} "
              f"{format_currency(s['total_profit']):>13} "
              f"{format_currency(s['avg_sales_per_customer']):>17}")

    print("\nTop 10 Customers:")
    for i, (customer, metrics) in enumerate(segments['top_10_customers'].items(), 1):
        print(f"{i:2}. {customer:<25} {format_currency(metrics['total_sales']):>12}")

    print_header("TOP 10 CITY MARKET ANALYSIS")

    cities = analytics.city_market_analysis()
    print(f"{'Rank':<6} {'City':<18} {'Region':<15} {'Sales':>13} {'Profit':>13} {'Margin':>8}")
    for i, city in enumerate(cities[:10], 1):
        print(f"{i:<6} {city['city']:<18} {city['region']:<15} "
              f"{format_currency(city['sales']):>13} {format_currency(city['profit']):>13} "
              f"{format_percent(city['margin']):>8}")

    print_header("DISCOUNT VS VOLUME CORRELATION BY CATEGORY")

    disc = analytics.discount_vs_volume_correlation()
    print(f"{'Category':<20} {'High Disc':>12} {'Low Disc':>12} {'Lift %':>10}")
    for cat, vals in disc.items():
        print(f"{cat:<20} {vals['high_discount_transactions']:>12} "
              f"{vals['low_discount_transactions']:>12} {format_percent(vals['volume_lift_pct']):>10}")

    print_header("PRODUCT SUBCATEGORY DEEP DIVE")

    deep_dive = analytics.product_subcategory_deep_dive()
    for category, items in list(deep_dive.items())[:3]:
        print(f"\n{category}:")
        print(f"{'Subcategory':<20} {'Sales':>15} {'Profit':>15} {'Margin':>10}")
        for item in items[:3]:
            print(f"{item['name']:<20} "
                  f"{format_currency(item['sales']):>15} "
                  f"{format_currency(item['profit']):>15} "
                  f"{format_percent(item['margin']):>10}")

    print_header("TEMPORAL TREND ANALYSIS")

    trends = analytics.temporal_trend_analysis()
    print("Yearly Performance:")
    print(f"{'Year':<6} {'Sales':>15} {'Profit':>15} {'Transactions':>15} {'Avg Order':>15}")

    for year, metrics in sorted(trends['yearly_performance'].items()):
        print(f"{year:<6} "
              f"{format_currency(metrics['sales']):>15} "
              f"{format_currency(metrics['profit']):>15} "
              f"{metrics['transactions']:>15} "
              f"{format_currency(metrics['avg_order_value']):>15}")

    print("\nYear-over-Year Growth:")
    for period, g in trends['growth_rates'].items():
        print(f"  {period}: Sales {format_percent(g['sales_growth'])}, "
              f"Profit {format_percent(g['profit_growth'])}")

    print_header("TOP 10 PRODUCT SUBCATEGORIES")

    top_subs = analytics.top_subcategories(10)
    print(f"{'Rank':<6} {'Subcategory':<20} {'Category':<15} {'Sales':>13}")
    for i, sub in enumerate(top_subs, 1):
        print(f"{i:<6} {sub['sub_category']:<20} {sub['category']:<15} "
              f"{format_currency(sub['sales']):>13}")

    print_header("MONTHLY SEASONALITY ANALYSIS")

    seasonality = analytics.monthly_seasonality_analysis()
    months = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    print(f"{'Month':<8} {'Sales':>13} {'Transactions':>13} {'Avg Trans':>13} {'Index':>8}")
    for month in sorted(seasonality):
        m = seasonality[month]
        print(f"{months[month]:<8} {format_currency(m['sales']):>13} "
              f"{m['transactions']:>13} {format_currency(m['avg_transaction']):>13} "
              f"{m['index']:>8.1f}")

    sys.stdout = original_stdout
    analysis_file.close()

    print("Analysis saved to analysis.txt")

    result = subprocess.run(
        [sys.executable, '-m', 'unittest', 'tests.test_analytics', '-v'],
        capture_output=True,
        text=True,
        cwd=project_root
    )

    with open(os.path.join(project_root, "unit_test_results.txt"), "w") as f:
        f.write(result.stdout + result.stderr)

    if result.returncode == 0:
        print("All tests passed. Full details saved to unit_test_results.txt")
    else:
        print("Some tests failed. See unit_test_results.txt for details.")


if __name__ == "__main__":
    main()
