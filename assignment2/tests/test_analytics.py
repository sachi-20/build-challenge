import unittest
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from sales_record import SalesRecord
from sales_analytics import SalesAnalytics
from csv_loader import CSVLoader


class TestSalesRecord(unittest.TestCase):
    """Unit tests for SalesRecord data model and computed properties."""

    def setUp(self):
        """Creates a reusable SalesRecord instance for test cases."""
        self.record = SalesRecord(
            order_id="TEST001",
            customer_name="Test Customer",
            category="Test Category",
            sub_category="Test Sub",
            city="Test City",
            order_date=datetime(2020, 1, 15),
            region="Test Region",
            sales=1000.0,
            discount=0.15,
            profit=200.0,
            state="Test State"
        )

    def test_profit_margin(self):
        """Validates correct profit margin calculation."""
        self.assertAlmostEqual(self.record.profit_margin, 20.0, places=2)

    def test_year_property(self):
        """Checks correct extraction of year from order date."""
        self.assertEqual(self.record.year, 2020)

    def test_month_property(self):
        """Checks correct extraction of month from order date."""
        self.assertEqual(self.record.month, 1)

    def test_discount_category_low(self):
        """Verifies Low discount classification."""
        self.record.discount = 0.05
        self.assertEqual(self.record.discount_category, "Low")

    def test_discount_category_medium(self):
        """Verifies Medium discount classification."""
        self.record.discount = 0.15
        self.assertEqual(self.record.discount_category, "Medium")

    def test_discount_category_high(self):
        """Verifies High discount classification."""
        self.record.discount = 0.25
        self.assertEqual(self.record.discount_category, "High")


class TestCSVLoader(unittest.TestCase):
    """Unit tests for CSVLoader date parsing functionality."""

    def test_parse_date_formats(self):
        """Tests valid date formats supported by CSVLoader."""
        dates = [
            ("11-08-2017", datetime(2017, 11, 8)),
            ("06-12-2017", datetime(2017, 6, 12)),
            ("11/22/2016", datetime(2016, 11, 22))
        ]

        for date_str, expected in dates:
            result = CSVLoader.parse_date(date_str)
            self.assertEqual(result, expected)

    def test_parse_date_invalid(self):
        """Ensures invalid date formats raise ValueError."""
        with self.assertRaises(ValueError):
            CSVLoader.parse_date("invalid-date")


class TestSalesAnalytics(unittest.TestCase):
    """Unit tests for SalesAnalytics core analytical methods."""

    def setUp(self):
        """Creates sample transaction records and SalesAnalytics object."""
        self.records = [
            SalesRecord("OD1", "Alice", "Food", "Grains", "CityA",
                        datetime(2020, 1, 1), "North", 1000, 0.05, 200, "StateA"),
            SalesRecord("OD2", "Bob", "Food", "Grains", "CityB",
                        datetime(2020, 2, 1), "South", 1500, 0.15, 300, "StateB"),
            SalesRecord("OD3", "Charlie", "Beverage", "Juice", "CityA",
                        datetime(2020, 3, 1), "North", 800, 0.2, 150, "StateA"),
            SalesRecord("OD4", "Alice", "Beverage", "Soda", "CityC",
                        datetime(2021, 1, 1), "East", 1200, 0.25, 250, "StateC"),
            SalesRecord("OD5", "David", "Food", "Flour", "CityB",
                        datetime(2021, 2, 1), "South", 900, 0.3, 180, "StateB")
        ]
        self.analytics = SalesAnalytics(self.records)

    def test_summary_statistics(self):
        """Validates summary statistics aggregation."""
        stats = self.analytics.summary_statistics()
        self.assertEqual(stats['sales']['total'], 5400.0)
        self.assertAlmostEqual(stats['sales']['mean'], 1080.0, places=2)
        self.assertGreater(stats['sales']['std_dev'], 0)

    def test_category_performance_matrix(self):
        """Tests category-based aggregation results."""
        result = self.analytics.category_performance_matrix()
        self.assertEqual(result["Food"]['total_sales'], 3400.0)
        self.assertEqual(result["Beverage"]['total_sales'], 2000.0)

    def test_regional_efficiency_analysis(self):
        """Validates regional aggregation and totals."""
        result = self.analytics.regional_efficiency_analysis()
        self.assertEqual(result["North"]['total_sales'], 1800.0)
        self.assertEqual(result["South"]['total_sales'], 2400.0)
        self.assertEqual(result["East"]['total_sales'], 1200.0)

    def test_discount_optimization_analysis(self):
        """Ensures discount brackets are correctly computed."""
        result = self.analytics.discount_optimization_analysis()
        self.assertIn("0-15%", result)
        self.assertIn("15-20%", result)

    def test_customer_segmentation_analysis(self):
        """Validates customer segmentation structure."""
        result = self.analytics.customer_segmentation_analysis()
        self.assertIn('high_value', result)
        self.assertIn('medium_value', result)
        self.assertIn('low_value', result)
        self.assertIn('top_10_customers', result)

    def test_product_subcategory_deep_dive(self):
        """Checks subcategory deep dive output."""
        result = self.analytics.product_subcategory_deep_dive()
        self.assertIn("Food", result)
        self.assertIn("Beverage", result)
        self.assertGreater(len(result["Food"]), 0)

    def test_top_subcategories(self):
        """Validates top N subcategory extraction."""
        result = self.analytics.top_subcategories(3)
        self.assertEqual(len(result), 3)
        self.assertIn('sub_category', result[0])

    def test_temporal_trend_analysis(self):
        """Validates yearly sales aggregation."""
        result = self.analytics.temporal_trend_analysis()
        self.assertEqual(result['yearly_performance'][2020]['sales'], 3300.0)
        self.assertEqual(result['yearly_performance'][2021]['sales'], 2100.0)

    def test_profitability_drivers_analysis(self):
        """Checks high and low margin segmentation logic."""
        result = self.analytics.profitability_drivers_analysis()
        self.assertIn('high_margin_segment', result)
        self.assertIn('low_margin_segment', result)

    def test_city_market_analysis(self):
        """Validates city-level market aggregation."""
        result = self.analytics.city_market_analysis()
        self.assertGreater(len(result), 0)
        self.assertIn('city', result[0])
        self.assertIn('sales', result[0])

    def test_discount_vs_volume_correlation(self):
        """Validates discount versus volume relationship."""
        result = self.analytics.discount_vs_volume_correlation()
        self.assertIn("Food", result)
        self.assertIn("Beverage", result)

    def test_monthly_seasonality_analysis(self):
        """Validates monthly transaction aggregation."""
        result = self.analytics.monthly_seasonality_analysis()
        self.assertEqual(result[1]['transactions'], 2)
        self.assertEqual(result[2]['transactions'], 2)
        self.assertEqual(result[3]['transactions'], 1)

    def test_filter(self):
        """Validates record filtering with predicate."""
        filtered = self.analytics.filter(lambda r: r.sales > 1000)
        self.assertEqual(filtered.count(), 2)

    def test_map(self):
        """Validates mapping operation on records."""
        cities = self.analytics.map(lambda r: r.city)
        self.assertEqual(len(cities), 5)
        self.assertIn("CityA", cities)

    def test_count(self):
        """Validates total record count."""
        self.assertEqual(self.analytics.count(), 5)

    def test_filter_chain(self):
        """Validates chaining of multiple filters."""
        result = (self.analytics
                  .filter(lambda r: r.region == "North")
                  .filter(lambda r: r.sales > 900))
        self.assertEqual(result.count(), 1)


if __name__ == '__main__':
    """Executes the unit test suite."""
    unittest.main()
