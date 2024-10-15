# test_knowledge_base.py
import unittest
from knowledge_base import SharedKnowledgeBase
class TestSharedKnowledgeBase(unittest.TestCase):
    def setUp(self):
        self.knowledge_base = SharedKnowledgeBase()
    def test_store_and_retrieve_knowledge(self):
        self.knowledge_base.store("test_key", "test_value")
        retrieved_value = self.knowledge_base.retrieve("test_key")
        self.assertEqual(retrieved_value, "test_value")
    def test_retrieve_non_existent_key(self):
        result = self.knowledge_base.retrieve("non_existent_key")
        self.assertIsNone(result)
    def test_remove_knowledge(self):
        self.knowledge_base.store("temp_key", "temp_value")
        self.knowledge_base.remove("temp_key")
        result = self.knowledge_base.retrieve("temp_key")
        self.assertIsNone(result)
if __name__ == '__main__':
    unittest.main()
