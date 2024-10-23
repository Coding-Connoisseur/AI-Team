# test_load_balancer.py
import unittest
from load_balancer import LoadBalancer
from agents import BaseAgent
class TestLoadBalancer(unittest.TestCase):
    def setUp(self):
        self.mock_agents = [BaseAgent("Agent1", {}), BaseAgent("Agent2", {})]
        self.load_balancer = LoadBalancer(self.mock_agents)
    def test_distribute_task_evenly(self):
        tasks = ["task1", "task2", "task3", "task4"]
        assignments = self.load_balancer.distribute_tasks(tasks)
        self.assertEqual(len(assignments), len(tasks))
    def test_assign_task_to_least_loaded_agent(self):
        task = "new_task"
        agent = self.load_balancer.assign_task(task)
        self.assertIn(agent, self.mock_agents)
    def test_update_agent_load(self):
        self.load_balancer.update_agent_load("Agent1", 5)
        self.assertEqual(self.load_balancer.agent_load["Agent1"], 5)
if __name__ == '__main__':
    unittest.main()
