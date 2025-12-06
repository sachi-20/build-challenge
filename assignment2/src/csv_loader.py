import csv
from datetime import datetime
from typing import List
from sales_record import SalesRecord


class CSVLoader:
    """
    Utility class for loading and parsing sales data from CSV files.
    """

    @staticmethod
    def parse_date(date_str: str) -> datetime:
        """
        Parses a date string into a datetime object using supported formats.
        Raises ValueError if the format is invalid.
        """
        date_str = date_str.strip()
        formats = ['%m-%d-%Y', '%d-%m-%Y', '%m/%d/%Y', '%d/%m/%Y']
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        raise ValueError(f"Unable to parse date: {date_str}")

    @staticmethod
    def load_sales_data(filepath: str) -> List[SalesRecord]:
        """
        Loads sales records from a CSV file and returns a list of SalesRecord objects.
        Skips malformed rows.
        """
        records: List[SalesRecord] = []

        with open(filepath, 'r', encoding='utf-8-sig', newline='') as file:
            reader = csv.DictReader(file)

            for row in reader:
                try:
                    record = SalesRecord(
                        order_id=row['Order ID'].strip(),
                        customer_name=row['Customer Name'].strip(),
                        category=row['Category'].strip(),
                        sub_category=row['Sub Category'].strip(),
                        city=row['City'].strip(),
                        order_date=CSVLoader.parse_date(row['Order Date']),
                        region=row['Region'].strip(),
                        sales=float(row['Sales']),
                        discount=float(row['Discount']),
                        profit=float(row['Profit']),
                        state=row['State'].strip()
                    )
                    records.append(record)

                except (ValueError, KeyError):
                    continue

        return records
