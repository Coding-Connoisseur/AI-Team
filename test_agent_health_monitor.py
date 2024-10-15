# test_agent_health_monitor.py
import unittest
from agent_health_monitor import AgentHealthMonitor, LoadBalancer
from agents import BaseAgent
class TestAgentHealthMonitor(unittest.TestCase):
    def setUp(self):
        self.mock_agents = [BaseAgent("TestAgent", {})]
        self.load_balancer = LoadBalancer(self.mock_agents)
        self.agent_health_monitor = AgentHealthMonitor(self.mock_agents, self.load_balancer)
    def test_record_task_success(self):
        self.agent_health_monitor.record_task("TestAgent", "success")
        health = self.agent_health_monitor.agent_health["TestAgent"]
        self.assertEqual(health["successes"], 1)
    def test_record_task_failure(self):
        self.agent_health_monitor.record_task("TestAgent", "failure")
        health = self.agent_health_monitor.agent_health["TestAgent"]
        self.assertEqual(health["failures"], 1)
    def test_trigger_rebalance_on_failure(self):
        self.agent_health_monitor.record_task("TestAgent", "failure")
        self.agent_health_monitor.record_task("TestAgent", "failure")
        self.agent_health_monitor.record_task("TestAgent", "failure")
        # Test rebalance logic as needed
        # Add mock or print statements to confirm behavior
if __name__ == '__main__':
    unittest.main()
