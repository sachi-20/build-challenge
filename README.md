# Programming Challenge Submissions

This repository contains completed solutions for two coding challenge assignments demonstrating concurrent programming and functional data analysis.

Prepared by Sachi Kaushik

## Assignments

### Assignment 1: Producer-Consumer Pattern

**Location:** `/assignment1/`

Implementation of the classic producer-consumer problem with thread synchronization using Python.

**Key Features:**

- Thread-safe bounded buffer with condition variables
- Wait/notify synchronization mechanism
- Poison pill pattern for clean shutdown
- Comprehensive unit tests

**Run:**

```bash
cd producer-consumer
python producer_consumer.py
python -m unittest tests/test_producer_consumer.py -v
```

### Assignment 2: Grocery Sales Analysis

**Location:** `/assignment2/`

Functional programming analysis of 10,000 grocery sales transactions using Python streams and aggregation.

**Key Features:**

- 12 business analytics operations
- Stream-based data processing with map/filter/reduce
- Statistical reporting and trend analysis
- 22 unit tests

**Run:**

```bash
cd grocery-sales
python src/main.py  # Runs analysis and tests
```

## Technologies

- **Language:** Python 3.7+
- **Dependencies:** Standard library only
- **Testing:** unittest

## Repository Structure

```
.
├── producer-consumer/
│   ├── producer_consumer.py
│   ├── tests/
│   └── README.md
│
├── grocery-sales/
│   ├── src/
│   ├── data/
│   ├── tests/
│   └── README.md
│
└── README.md (this file)
```

## Assignment Requirements Met

- Python implementation
- Thread synchronization and concurrent programming
- Functional programming with streams
- Data aggregation and lambda expressions
- Comprehensive unit tests
- Documentation and setup instructions
- Console output and results

Each assignment has its own detailed README with specific implementation details, usage examples, and design decisions.
