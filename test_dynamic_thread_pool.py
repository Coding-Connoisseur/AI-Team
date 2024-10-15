# test_dynamic_thread_pool.py
import unittest
from dynamic_thread_pool import DynamicThreadPoolExecutor
import time
class TestDynamicThreadPoolExecutor(unittest.TestCase):
    def setUp(self):
        self.pool = DynamicThreadPoolExecutor(max_workers=3)
    def tearDown(self):
        self.pool.shutdown()
    def test_submit_task(self):
        def sample_task(x):
            return x * 2
        future = self.pool.submit(sample_task, 5)
        result = future.result()
        self.assertEqual(result, 10)
    def test_adjust_worker_count(self):
        initial_count = self.pool._max_workers
        self.pool.adjust_worker_count(5)
        self.assertEqual(self.pool._max_workers, 5)
    def test_task_execution_with_delay(self):
        def delayed_task():
            time.sleep(1)
            return "completed"
        future = self.pool.submit(delayed_task)
        result = future.result()
        self.assertEqual(result, "completed")
if __name__ == '__main__':
    unittest.main()
