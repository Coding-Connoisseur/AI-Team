# test_system.py
import unittest
from system import System
class TestSystem(unittest.TestCase):
    def setUp(self):
        self.system = System()
    def test_get_cpu_usage(self):
        cpu_usage = self.system.get_cpu_usage()
        self.assertIsInstance(cpu_usage, float)
        self.assertGreaterEqual(cpu_usage, 0.0)
    def test_get_memory_usage(self):
        memory_usage = self.system.get_memory_usage()
        self.assertIsInstance(memory_usage, float)
        self.assertGreaterEqual(memory_usage, 0.0)
    def test_get_disk_usage(self):
        disk_usage = self.system.get_disk_usage()
        self.assertIsInstance(disk_usage, float)
        self.assertGreaterEqual(disk_usage, 0.0)
    def test_get_network_usage(self):
        network_usage = self.system.get_network_usage()
        self.assertIsInstance(network_usage, float)
        self.assertGreaterEqual(network_usage, 0.0)
if __name__ == '__main__':
    unittest.main()
