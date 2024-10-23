# test_task_monitor.py
import unittest
from task_monitor import TaskMonitor
from agents import BaseAgent
class TestTaskMonitor(unittest.TestCase):
    def setUp(self):
        self.agent = BaseAgent("TestAgent", {})
        self.task_monitor = TaskMonitor(self.agent)
    def test_start_task(self):
        task_name = "sample_task"
        self.task_monitor.start_task(task_name)
        self.assertEqual(self.task_monitor.current_task, task_name)
    def test_complete_task(self):
        task_name = "sample_task"
        self.task_monitor.start_task(task_name)
        self.task_monitor.complete_task("success")
        self.assertIsNone(self.task_monitor.current_task)
        self.assertIn("success", self.task_monitor.task_history)
    def test_task_failure(self):
        task_name = "sample_task"
        self.task_monitor.start_task(task_name)
        self.task_monitor.complete_task("failure")
        self.assertIn("failure", self.task_monitor.task_history)
if __name__ == '__main__':
    unittest.main()
