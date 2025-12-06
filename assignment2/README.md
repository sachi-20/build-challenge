# Grocery Sales Analysis

## Assignment Deliverables

1. Public GitHub repository
2. Complete source code
3. Unit tests for all analysis methods
4. README with setup instructions and sample output
5. Results of all analyses printed to console and saved to file

## Overview

This Python application performs end-to-end grocery retail sales analysis using functional programming principles. It demonstrates stream-style operations, grouping, aggregation, lambda expressions, and statistical reporting using only the Python standard library.

The program loads nearly 10,000 transactions from a CSV file, performs multiple business analyses, prints formatted results to the console, saves them to a file, and executes unit tests automatically.

## Project Structure

```
grocery-sales-clean/
├── README.md
├── analysis.txt                   # Generated output from main.py
├── data/
│   └── sales_data.csv             # Dataset (9,994 records)
├── src/
│   ├── sales_record.py            # Data model with computed properties
│   ├── csv_loader.py              # CSV parsing and date handling
│   ├── sales_analytics.py         # Core analytics methods
│   └── main.py                    # Main application
└── tests/
    └── test_analytics.py          # Unit tests (22 tests)
```

## Quick Start

```bash
# Navigate to project root
cd grocery-sales-clean

# Run full analysis (also runs unit tests)
python src/main.py

# Run tests separately if needed
python -m unittest tests.test_analytics -v
```

## Output

Running `python src/main.py` produces:

* Complete formatted business analysis printed to console
* Full output saved to `analysis.txt`
* Automatic execution of all unit tests
* Confirmation message when all tests pass

## Analyses Performed

1. Executive Statistical Summary
2. Category Performance Matrix
3. Regional Efficiency Analysis
4. Discount Optimization Analysis
5. Customer Segmentation Analysis
6. Product Subcategory Deep Dive
7. Temporal Trend Analysis (Year-over-Year Growth)
8. Profitability Drivers Analysis
9. City Market Analysis (Top 10)
10. Discount vs Volume Correlation
11. Top Product Subcategories
12. Monthly Seasonality Analysis

All results are formatted as readable business tables.

## Functional Programming Objectives

**Functional Programming**

* Extensive use of `reduce`, `map`, `filter`
* Lambda-based predicates and transformations
* Immutable record design

**Stream Operations**

* `groupby` for hierarchical grouping
* Iterator-based aggregation
* Chainable filtering and mapping

**Data Aggregation**

* Sum, mean, median, standard deviation
* Multi-level dimensional grouping
* Derived metrics such as margin and growth rates

**Lambda Expressions**

* Predicate functions
* Sorting keys
* Group transformations

## Unit Tests

**Total Tests:** 22

**SalesRecord Tests**

* Profit margin calculation
* Date property extraction
* Discount category classification

**CSV Loader Tests**

* Multiple date format parsing
* Invalid date handling

**SalesAnalytics Tests**

* All analytics methods
* Filter, map, and count operations
* Data integrity validation

Tests run automatically as part of `main.py` and can also be executed independently.

## Dataset

* **Source:** Supermart Grocery Sales Dataset
* **Records:** 9,994
* **Years:** 2015–2018
* **Categories:** 7
* **Subcategories:** 23
* **Cities:** 24
* **Regions:** 5
* **Customers:** 50

## Technical Implementation

**Python Version:** 3.7+

**Dependencies:** Standard library only

**Libraries Used:**

* `functools`
* `itertools`
* `operator`
* `statistics`

**Key Design Features:**

* Dataclass-based immutable records
* Pure functional analytics methods
* No external dependencies
* Type hints throughout
* Deterministic output

## Sample Output

Complete formatted output is available in **analysis.txt**, including:

* Statistical summaries
* Business performance matrices
* Trend and seasonality analysis
* Top customer and product breakdowns

Detailed unit test execution logs are saved in **unit_test_results.txt**, including:

* Full test case output
* Pass/fail status for each test
* Execution summary

All tests pass successfully.
