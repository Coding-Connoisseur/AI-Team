# test_health_check_manager.py
import unittest
from health_check_manager import HealthCheckManager
from agents import BaseAgent
class TestHealthCheckManager(unittest.TestCase):
    def setUp(self):
        self.mock_agents = [BaseAgent("Agent1", {}), BaseAgent("Agent2", {})]
        self.health_check_manager = HealthCheckManager(self.mock_agents)
    def test_health_check(self):
        results = self.health_check_manager.check_health()
        self.assertIsInstance(results, dict)
        self.assertIn("Agent1", results)
        self.assertIn("Agent2", results)
    def test_health_status(self):
        for agent in self.mock_agents:
            status = self.health_check_manager.get_health_status(agent.name)
            self.assertIn(status, ["healthy", "unhealthy"])
    def test_recover_unhealthy_agents(self):
        # Assuming there is logic to mark an agent as unhealthy
        unhealthy_agents = self.health_check_manager.recover_unhealthy_agents()
        self.assertIsInstance(unhealthy_agents, list)
if __name__ == '__main__':
    unittest.main()
