# test_task_priority_queue.py
import unittest
from task_priority_queue import TaskPriorityQueue
class TestTaskPriorityQueue(unittest.TestCase):
    def setUp(self):
        self.priority_queue = TaskPriorityQueue()
    def test_enqueue_task(self):
        self.priority_queue.enqueue("task1", priority=1)
        self.priority_queue.enqueue("task2", priority=3)
        self.priority_queue.enqueue("task3", priority=2)
        self.assertEqual(len(self.priority_queue.queue), 3)
    def test_dequeue_task(self):
        self.priority_queue.enqueue("task1", priority=1)
        self.priority_queue.enqueue("task2", priority=3)
        task = self.priority_queue.dequeue()
        self.assertEqual(task, "task1")
    def test_queue_emptiness(self):
        self.priority_queue.enqueue("task1", priority=1)
        self.priority_queue.dequeue()
        self.assertTrue(self.priority_queue.is_empty())
    def test_peek_task(self):
        self.priority_queue.enqueue("task1", priority=1)
        self.priority_queue.enqueue("task2", priority=3)
        task = self.priority_queue.peek()
        self.assertEqual(task, "task1")
if __name__ == '__main__':
    unittest.main()
