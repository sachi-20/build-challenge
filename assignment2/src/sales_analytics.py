from typing import List, Dict, Callable, Any
from functools import reduce
from itertools import groupby
from operator import attrgetter, itemgetter
from statistics import mean, median, stdev
from sales_record import SalesRecord


class SalesAnalytics:
    """
    Provides analytics operations using functional programming patterns.
    """

    def __init__(self, records: List[SalesRecord]):
        """Initializes the analytics engine with sales records."""
        self.records = records

    def summary_statistics(self) -> Dict[str, Dict[str, float]]:
        """Computes overall summary statistics for sales, profit, discount, and margin."""
        sales_list = list(map(lambda r: r.sales, self.records))
        profit_list = list(map(lambda r: r.profit, self.records))
        discount_list = list(map(lambda r: r.discount, self.records))
        margin_list = list(map(lambda r: r.profit_margin, self.records))

        return {
            'sales': {
                'total': reduce(lambda acc, x: acc + x, sales_list, 0.0),
                'mean': mean(sales_list),
                'median': median(sales_list),
                'std_dev': stdev(sales_list) if len(sales_list) > 1 else 0,
                'min': min(sales_list),
                'max': max(sales_list)
            },
            'profit': {
                'total': reduce(lambda acc, x: acc + x, profit_list, 0.0),
                'mean': mean(profit_list),
                'median': median(profit_list),
                'std_dev': stdev(profit_list) if len(profit_list) > 1 else 0,
                'min': min(profit_list),
                'max': max(profit_list)
            },
            'discount': {
                'mean': mean(discount_list),
                'median': median(discount_list),
                'min': min(discount_list),
                'max': max(discount_list)
            },
            'profit_margin': {
                'mean': mean(margin_list),
                'median': median(margin_list)
            }
        }

    def category_performance_matrix(self) -> Dict[str, Dict[str, Any]]:
        """Aggregates sales and profit metrics by product category."""
        sorted_records = sorted(self.records, key=attrgetter('category'))
        result = {}

        for category, group in groupby(sorted_records, key=attrgetter('category')):
            group_list = list(group)
            total_sales = sum(r.sales for r in group_list)
            total_profit = sum(r.profit for r in group_list)

            result[category] = {
                'total_sales': total_sales,
                'total_profit': total_profit,
                'profit_margin': (total_profit / total_sales * 100) if total_sales else 0,
                'transaction_count': len(group_list)
            }

        return dict(sorted(result.items(), key=lambda x: x[1]['total_sales'], reverse=True))

    def regional_efficiency_analysis(self) -> Dict[str, Dict[str, float]]:
        """Analyzes regional performance based on sales efficiency and customer reach."""
        sorted_records = sorted(self.records, key=attrgetter('region'))
        result = {}

        for region, group in groupby(sorted_records, key=attrgetter('region')):
            group_list = list(group)
            total_sales = sum(r.sales for r in group_list)
            total_profit = sum(r.profit for r in group_list)

            result[region] = {
                'total_sales': total_sales,
                'total_profit': total_profit,
                'profit_margin': (total_profit / total_sales * 100) if total_sales else 0,
                'cities_served': len(set(r.city for r in group_list)),
                'unique_customers': len(set(r.customer_name for r in group_list))
            }

        return dict(sorted(result.items(), key=lambda x: x[1]['profit_margin'], reverse=True))

    def discount_optimization_analysis(self) -> Dict[str, Any]:
        """Evaluates profitability across predefined discount brackets."""
        brackets = [
            ('0-15%', lambda r: r.discount < 0.15),
            ('15-20%', lambda r: 0.15 <= r.discount < 0.20),
            ('20-25%', lambda r: 0.20 <= r.discount < 0.25),
            ('25-30%', lambda r: 0.25 <= r.discount < 0.30),
            ('30%+', lambda r: r.discount >= 0.30)
        ]

        result = {}
        for name, predicate in brackets:
            records = list(filter(predicate, self.records))
            if not records:
                continue

            total_sales = sum(r.sales for r in records)
            total_profit = sum(r.profit for r in records)

            result[name] = {
                'transaction_count': len(records),
                'total_sales': total_sales,
                'total_profit': total_profit,
                'profit_margin': (total_profit / total_sales * 100) if total_sales else 0
            }

        return result

    def customer_segmentation_analysis(self) -> Dict[str, Any]:
        """Segments customers into high, medium, and low value groups."""
        sorted_records = sorted(self.records, key=attrgetter('customer_name'))
        customer_metrics = {}

        for customer, group in groupby(sorted_records, key=attrgetter('customer_name')):
            group_list = list(group)
            total_sales = sum(r.sales for r in group_list)
            total_profit = sum(r.profit for r in group_list)

            customer_metrics[customer] = {
                'total_sales': total_sales,
                'total_profit': total_profit,
                'transaction_count': len(group_list)
            }

        sorted_customers = sorted(customer_metrics.items(), key=lambda x: x[1]['total_sales'], reverse=True)
        total_customers = len(sorted_customers)

        high = dict(sorted_customers[:int(total_customers * 0.2)])
        mid = dict(sorted_customers[int(total_customers * 0.2):int(total_customers * 0.5)])
        low = dict(sorted_customers[int(total_customers * 0.5):])

        def summarize(segment):
            """Summarizes aggregated metrics for a customer segment."""
            total_sales = sum(m['total_sales'] for m in segment.values())
            total_profit = sum(m['total_profit'] for m in segment.values())

            return {
                'customer_count': len(segment),
                'total_sales': total_sales,
                'total_profit': total_profit,
                'avg_sales_per_customer': total_sales / len(segment) if segment else 0
            }

        return {
            'high_value': summarize(high),
            'medium_value': summarize(mid),
            'low_value': summarize(low),
            'top_10_customers': dict(sorted_customers[:10])
        }

    def product_subcategory_deep_dive(self) -> Dict[str, List[Dict[str, Any]]]:
        """Provides detailed performance metrics for each product subcategory."""
        sorted_records = sorted(self.records, key=lambda r: (r.category, r.sub_category))
        result = {}

        for category, cat_group in groupby(sorted_records, key=attrgetter('category')):
            cat_list = list(cat_group)
            cat_list.sort(key=attrgetter('sub_category'))

            subcats = []
            for subcat, sub_group in groupby(cat_list, key=attrgetter('sub_category')):
                sub_list = list(sub_group)

                total_sales = sum(r.sales for r in sub_list)
                total_profit = sum(r.profit for r in sub_list)

                subcats.append({
                    'name': subcat,
                    'sales': total_sales,
                    'profit': total_profit,
                    'margin': (total_profit / total_sales * 100) if total_sales else 0
                })

            result[category] = sorted(subcats, key=lambda x: x['sales'], reverse=True)

        return result

    def temporal_trend_analysis(self) -> Dict[str, Any]:
        """Calculates yearly performance and growth trends."""
        sorted_by_year = sorted(self.records, key=attrgetter('year'))
        yearly_data = {}

        for year, group in groupby(sorted_by_year, key=attrgetter('year')):
            group_list = list(group)
            total_sales = sum(r.sales for r in group_list)
            total_profit = sum(r.profit for r in group_list)

            yearly_data[year] = {
                'sales': total_sales,
                'profit': total_profit,
                'transactions': len(group_list),
                'avg_order_value': total_sales / len(group_list)
            }

        years = sorted(yearly_data.keys())
        growth_rates = {}

        for i in range(1, len(years)):
            prev, curr = years[i - 1], years[i]
            growth_rates[f"{prev}-{curr}"] = {
                'sales_growth': ((yearly_data[curr]['sales'] - yearly_data[prev]['sales']) /
                                 yearly_data[prev]['sales']) * 100,
                'profit_growth': ((yearly_data[curr]['profit'] - yearly_data[prev]['profit']) /
                                  yearly_data[prev]['profit']) * 100
            }

        return {
            'yearly_performance': yearly_data,
            'growth_rates': growth_rates
        }

    def profitability_drivers_analysis(self) -> Dict[str, Any]:
        """Identifies key drivers for high and low profit margin segments."""
        high = list(filter(lambda r: r.profit_margin > 25, self.records))
        low = list(filter(lambda r: r.profit_margin <= 25, self.records))

        def analyze(records):
            """Summarizes profit characteristics for a given record set."""
            if not records:
                return None

            total_sales = sum(r.sales for r in records)
            total_profit = sum(r.profit for r in records)

            categories = {}
            for r in records:
                categories[r.category] = categories.get(r.category, 0) + 1

            return {
                'transaction_count': len(records),
                'total_sales': total_sales,
                'total_profit': total_profit,
                'avg_profit_margin': mean(r.profit_margin for r in records),
                'avg_discount': mean(r.discount for r in records),
                'dominant_category': max(categories.items(), key=itemgetter(1))[0]
            }

        return {
            'high_margin_segment': analyze(high),
            'low_margin_segment': analyze(low)
        }

    def city_market_analysis(self) -> List[Dict[str, Any]]:
        """Ranks cities based on total sales and profitability."""
        sorted_records = sorted(self.records, key=attrgetter('city'))
        city_data = []

        for city, group in groupby(sorted_records, key=attrgetter('city')):
            group_list = list(group)
            total_sales = sum(r.sales for r in group_list)
            total_profit = sum(r.profit for r in group_list)

            city_data.append({
                'city': city,
                'region': group_list[0].region,
                'sales': total_sales,
                'profit': total_profit,
                'margin': (total_profit / total_sales * 100) if total_sales else 0,
                'unique_customers': len(set(r.customer_name for r in group_list))
            })

        return sorted(city_data, key=lambda x: x['sales'], reverse=True)

    def discount_vs_volume_correlation(self) -> Dict[str, Any]:
        """Measures transaction volume differences between high and low discount levels."""
        sorted_records = sorted(self.records, key=attrgetter('category'))
        result = {}

        for category, group in groupby(sorted_records, key=attrgetter('category')):
            group_list = list(group)
            high = [r for r in group_list if r.discount >= 0.25]
            low = [r for r in group_list if r.discount < 0.15]

            result[category] = {
                'high_discount_transactions': len(high),
                'low_discount_transactions': len(low),
                'volume_lift_pct': ((len(high) - len(low)) / len(low) * 100) if low else 0
            }

        return result

    def top_subcategories(self, limit: int = 10):
        """Returns the top-performing product subcategories by sales volume."""
        sorted_records = sorted(self.records, key=attrgetter('sub_category'))
        subcat_data = []

        for subcat, group in groupby(sorted_records, key=attrgetter('sub_category')):
            group_list = list(group)

            total_sales = sum(r.sales for r in group_list)
            total_profit = sum(r.profit for r in group_list)

            subcat_data.append({
                "sub_category": subcat,
                "category": group_list[0].category,
                "sales": total_sales,
                "profit": total_profit,
                "margin": (total_profit / total_sales * 100) if total_sales else 0,
                "transactions": len(group_list)
            })

        subcat_data.sort(key=lambda x: x["sales"], reverse=True)
        return subcat_data[:limit]

    def monthly_seasonality_analysis(self) -> Dict[int, Dict[str, float]]:
        """Computes monthly sales seasonality indices."""
        sorted_by_month = sorted(self.records, key=attrgetter('month'))
        monthly_data = {}

        for month, group in groupby(sorted_by_month, key=attrgetter('month')):
            group_list = list(group)
            total_sales = sum(r.sales for r in group_list)

            monthly_data[month] = {
                'sales': total_sales,
                'transactions': len(group_list),
                'avg_transaction': total_sales / len(group_list)
            }

        avg_monthly_sales = mean(m['sales'] for m in monthly_data.values())

        for month in monthly_data:
            monthly_data[month]['index'] = (monthly_data[month]['sales'] / avg_monthly_sales) * 100

        return monthly_data

    def filter(self, predicate: Callable[[SalesRecord], bool]) -> 'SalesAnalytics':
        """Filters records using a predicate and returns a new SalesAnalytics object."""
        return SalesAnalytics(list(filter(predicate, self.records)))

    def map(self, mapper: Callable[[SalesRecord], Any]) -> list:
        """Applies a mapping function over all records."""
        return list(map(mapper, self.records))

    def count(self) -> int:
        """Returns the total number of records."""
        return len(self.records)
