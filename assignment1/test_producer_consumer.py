"""
Test suite for producer-consumer implementation.

Tests thread synchronization, blocking behavior, concurrent access,
and data integrity.


"""

import threading
import time
import unittest
from collections import Counter

from producer_consumer import (
    BoundedBuffer,
    SourceContainer,
    DestinationContainer,
    Producer,
    Consumer,
    BufferTimeoutError,
)


class TestBoundedBuffer(unittest.TestCase):
    """Test BoundedBuffer synchronization primitives."""
    
    def test_put_take_single_item(self):
        """Basic sanity check."""
        buf = BoundedBuffer(1)
        buf.put(42)
        self.assertEqual(buf.take(), 42)
        self.assertEqual(buf.size(), 0)
    
    def test_fifo_order(self):
        """Buffer maintains FIFO order."""
        buf = BoundedBuffer(5)
        items = [1, 2, 3, 4, 5]
        
        for item in items:
            buf.put(item)
        
        result = []
        for _ in range(5):
            result.append(buf.take())
        
        self.assertEqual(result, items)
    
    def test_consumer_blocks_on_empty(self):
        """Consumer blocks when buffer is empty."""
        buf = BoundedBuffer(1)
        result = []
        
        def consumer():
            result.append(buf.take())
        
        t = threading.Thread(target=consumer)
        t.start()
        
        time.sleep(0.1)
        self.assertEqual(result, [], "Consumer should block on empty buffer")
        
        buf.put(99)
        t.join(timeout=1.0)
        self.assertFalse(t.is_alive())
        self.assertEqual(result, [99])
    
    def test_producer_blocks_on_full(self):
        """Producer blocks when buffer is full."""
        buf = BoundedBuffer(1)
        buf.put(1)
        finished = []
        
        def producer():
            buf.put(2)
            finished.append(True)
        
        t = threading.Thread(target=producer)
        t.start()
        
        time.sleep(0.1)
        self.assertEqual(finished, [], "Producer should block on full buffer")
        
        buf.take()
        t.join(timeout=1.0)
        self.assertFalse(t.is_alive())
        self.assertEqual(finished, [True])
    
    def test_capacity_not_exceeded(self):
        """Buffer size never exceeds capacity under concurrent access."""
        capacity = 3
        buf = BoundedBuffer(capacity)
        stop = False
        violations = []
        
        def producer():
            i = 0
            while not stop:
                buf.put(i)
                i += 1
        
        def consumer():
            while not stop:
                buf.take()
        
        p = threading.Thread(target=producer)
        c = threading.Thread(target=consumer)
        
        p.start()
        c.start()
        
        for _ in range(100):
            time.sleep(0.01)
            if buf.size() > capacity:
                violations.append(buf.size())
                break
        
        stop = True
        time.sleep(0.1)
        p.join(timeout=1.0)
        c.join(timeout=1.0)
        
        self.assertEqual(violations, [], f"Capacity violated: {violations}")
    
    def test_take_timeout(self):
        """take() with timeout raises BufferTimeoutError."""
        buf = BoundedBuffer(1)
        start = time.monotonic()
        
        with self.assertRaises(BufferTimeoutError):
            buf.take(timeout=0.2)
        
        elapsed = time.monotonic() - start
        self.assertGreaterEqual(elapsed, 0.18)
        self.assertLess(elapsed, 0.5)
    
    def test_put_timeout(self):
        """put() with timeout raises BufferTimeoutError."""
        buf = BoundedBuffer(1)
        buf.put(1)
        start = time.monotonic()
        
        with self.assertRaises(BufferTimeoutError):
            buf.put(2, timeout=0.2)
        
        elapsed = time.monotonic() - start
        self.assertGreaterEqual(elapsed, 0.18)
        self.assertLess(elapsed, 0.5)


class TestSourceContainer(unittest.TestCase):
    """Test SourceContainer thread safety."""
    
    def test_sequential_access(self):
        """Items returned in order."""
        source = SourceContainer([1, 2, 3])
        self.assertEqual(source.get_next(), 1)
        self.assertEqual(source.get_next(), 2)
        self.assertEqual(source.get_next(), 3)
        self.assertIsNone(source.get_next())
    
    def test_thread_safe_access(self):
        """Multiple threads can safely access source."""
        items = list(range(100))
        source = SourceContainer(items)
        result = []
        lock = threading.Lock()
        
        def getter():
            while True:
                item = source.get_next()
                if item is None:
                    break
                with lock:
                    result.append(item)
        
        threads = [threading.Thread(target=getter) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        self.assertEqual(sorted(result), items)


class TestDestinationContainer(unittest.TestCase):
    """Test DestinationContainer thread safety."""
    
    def test_concurrent_adds(self):
        """Multiple threads can safely add items."""
        dest = DestinationContainer()
        
        def adder(start, count):
            for i in range(start, start + count):
                dest.add(i)
        
        threads = [
            threading.Thread(target=adder, args=(i*25, 25))
            for i in range(4)
        ]
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        self.assertEqual(dest.size(), 100)
        self.assertEqual(sorted(dest.get_items()), list(range(100)))


class TestProducerConsumer(unittest.TestCase):
    """Test complete producer-consumer pipeline."""
    
    def test_single_producer_consumer(self):
        """All items transferred correctly."""
        data = list(range(10))
        source = SourceContainer(data)
        destination = DestinationContainer()
        buffer = BoundedBuffer(2)
        poison = object()
        
        producer = Producer(source, buffer, poison, name="P1")
        consumer = Consumer(buffer, destination, poison, name="C1")
        
        producer.start()
        consumer.start()
        
        producer.join(timeout=2.0)
        consumer.join(timeout=2.0)
        
        self.assertFalse(producer.is_alive())
        self.assertFalse(consumer.is_alive())
        self.assertEqual(destination.size(), source.size())
        self.assertEqual(destination.get_items(), data)
    
    def test_json_data_transfer(self):
        """JSON-like data transfers correctly."""
        data = [
            {"id": 1, "event": "login"},
            {"id": 2, "event": "click", "target": "/"},
            {"id": 3, "event": "logout"},
        ]
        
        source = SourceContainer(data)
        destination = DestinationContainer()
        buffer = BoundedBuffer(2)
        poison = object()
        
        producer = Producer(source, buffer, poison, name="P-JSON")
        consumer = Consumer(buffer, destination, poison, name="C-JSON")
        
        producer.start()
        consumer.start()
        producer.join(timeout=2.0)
        consumer.join(timeout=2.0)
        
        self.assertFalse(producer.is_alive())
        self.assertFalse(consumer.is_alive())
        self.assertEqual(destination.get_items(), data)
    
    def test_large_dataset(self):
        """Handles large dataset correctly."""
        data = list(range(100))
        source = SourceContainer(data)
        destination = DestinationContainer()
        buffer = BoundedBuffer(10)
        poison = object()
        
        producer = Producer(source, buffer, poison, name="P-Large")
        consumer = Consumer(buffer, destination, poison, name="C-Large")
        
        producer.start()
        consumer.start()
        producer.join(timeout=5.0)
        consumer.join(timeout=5.0)
        
        self.assertFalse(producer.is_alive())
        self.assertFalse(consumer.is_alive())
        self.assertEqual(destination.size(), 100)
        self.assertEqual(sorted(destination.get_items()), data)


class TestConcurrency(unittest.TestCase):
    """Test concurrent multi-producer/multi-consumer scenarios."""
    
    def test_multi_producer_multi_consumer(self):
        """Multiple producers and consumers maintain data integrity."""
        items_per_producer = 500
        buffer = BoundedBuffer(10)
        
        producer1_items = list(range(0, items_per_producer))
        producer2_items = list(range(items_per_producer, 2 * items_per_producer))
        all_items = producer1_items + producer2_items
        
        consumed = []
        consumed_lock = threading.Lock()
        poison = None
        
        def producer_fn(items):
            for x in items:
                buffer.put(x)
        
        def consumer_fn():
            while True:
                item = buffer.take()
                if item is poison:
                    break
                with consumed_lock:
                    consumed.append(item)
        
        p1 = threading.Thread(target=producer_fn, args=(producer1_items,))
        p2 = threading.Thread(target=producer_fn, args=(producer2_items,))
        c1 = threading.Thread(target=consumer_fn)
        c2 = threading.Thread(target=consumer_fn)
        
        p1.start()
        p2.start()
        c1.start()
        c2.start()
        
        p1.join(timeout=5.0)
        p2.join(timeout=5.0)
        self.assertFalse(p1.is_alive())
        self.assertFalse(p2.is_alive())
        
        for _ in range(2):
            buffer.put(poison)
        
        c1.join(timeout=5.0)
        c2.join(timeout=5.0)
        self.assertFalse(c1.is_alive())
        self.assertFalse(c2.is_alive())
        
        self.assertEqual(len(consumed), len(all_items))
        self.assertEqual(Counter(consumed), Counter(all_items))
    
    def test_stress_small_buffer(self):
        """Stress test with many items and small buffer."""
        total_items = 1000
        buffer = BoundedBuffer(1)
        
        num_producers = 2
        items_per_producer = total_items // num_producers
        
        producer_items = [
            list(range(i * items_per_producer, (i + 1) * items_per_producer))
            for i in range(num_producers)
        ]
        all_items = [x for sub in producer_items for x in sub]
        
        consumed = []
        consumed_lock = threading.Lock()
        poison = None
        
        def producer_fn(items):
            for x in items:
                buffer.put(x)
        
        def consumer_fn():
            while True:
                item = buffer.take()
                if item is poison:
                    break
                with consumed_lock:
                    consumed.append(item)
        
        producers = [
            threading.Thread(target=producer_fn, args=(items,))
            for items in producer_items
        ]
        consumers = [threading.Thread(target=consumer_fn) for _ in range(2)]
        
        for t in producers + consumers:
            t.start()
        
        for t in producers:
            t.join(timeout=10.0)
            self.assertFalse(t.is_alive())
        
        for _ in range(2):
            buffer.put(poison)
        
        for t in consumers:
            t.join(timeout=10.0)
            self.assertFalse(t.is_alive())
        
        self.assertEqual(len(consumed), len(all_items))
        self.assertEqual(Counter(consumed), Counter(all_items))


if __name__ == "__main__":
    unittest.main()
