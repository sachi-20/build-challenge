# Producer-Consumer Pattern

Implementation of the classic producer-consumer problem demonstrating thread synchronization and concurrent programming.

## Overview

This project implements a bounded buffer solution to the producer-consumer problem using Python's threading primitives. It demonstrates:

- Thread synchronization using condition variables (wait/notify)
- Blocking queues with proper mutual exclusion
- Concurrent data transfer between containers
- Safe shutdown using poison pill pattern

## Features

### Core Implementation

- **BoundedBuffer**: Thread-safe bounded queue using condition variables
- **SourceContainer**: Thread-safe source with sequential item retrieval
- **DestinationContainer**: Thread-safe destination for consumed items
- **Producer Thread**: Reads from source and places items in buffer
- **Consumer Thread**: Takes items from buffer and stores in destination

### Thread Synchronization

- Condition variables for wait/notify mechanism
- Blocking when buffer is full (producer waits)
- Blocking when buffer is empty (consumer waits)
- Mutual exclusion for all shared resources
- Optional timeout support to prevent indefinite blocking

### Data Support

Works with arbitrary Python objects:

- Integers
- Strings
- Dictionaries (JSON-like data)
- Custom objects
- Mixed types

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Run demonstrations

```bash
python producer_consumer.py
```

### Run tests

```bash
python -m unittest tests/test_producer_consumer.py -v
```

Or with pytest:

```bash
pytest tests/ -v
```

## Implementation Details

### BoundedBuffer

Thread-safe bounded buffer using condition variables:

```python
buffer = BoundedBuffer(capacity=5)

# Producer
buffer.put(item)

# Consumer  
item = buffer.take()

# With timeout
try:
    buffer.put(item, timeout=1.0)
except BufferTimeoutError:
    print("Timeout")
```

### Producer-Consumer Pipeline

```python
source = SourceContainer([1, 2, 3, 4, 5])
destination = DestinationContainer()
buffer = BoundedBuffer(capacity=3)

POISON_PILL = object()

producer = Producer(source, buffer, POISON_PILL, name="P1")
consumer = Consumer(buffer, destination, POISON_PILL, name="C1")

producer.start()
consumer.start()

producer.join()
consumer.join()

result = destination.get_items()
```

## Testing

Test suite includes:

- Unit tests for BoundedBuffer synchronization
- Thread-safety tests for containers
- Integration tests for complete pipeline
- Blocking behavior verification
- Multi-producer/multi-consumer scenarios
- Stress tests with high contention
- Timeout handling tests

Run tests:

```bash
python -m unittest tests/test_producer_consumer.py
```

## Project Structure

```
.
├── producer_consumer.py       # Main implementation
├── tests/
│   └── test_producer_consumer.py  # Test suite
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.7+
- No external dependencies for core functionality
- pytest (optional, for running tests)

## Design Decisions

### Condition Variables vs Queue

This implementation uses condition variables instead of `queue.Queue` to demonstrate manual synchronization and the wait/notify mechanism explicitly.

### Poison Pill Pattern

Uses a sentinel object to signal consumers when producers are done. This ensures clean shutdown without deadlocks or hanging threads.

### Timeout Support

Optional timeout parameters prevent indefinite blocking and allow applications to implement fallback behavior.
