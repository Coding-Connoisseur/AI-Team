# test_agents.py
import unittest
from agents import ProjectArchitectAI, CodeGeneratorAI, TestAI, DebuggingAI, EnhancerAI, DocumentationAI, DeploymentAI, SecurityAI, DatabaseAI, LoggingAI, VersionControlAI, FrontendGeneratorAI
from knowledge_base import SharedKnowledgeBase
class TestAgents(unittest.TestCase):
    def setUp(self):
        self.knowledge_base = SharedKnowledgeBase()
        self.agents = [
            ProjectArchitectAI(self.knowledge_base),
            CodeGeneratorAI(self.knowledge_base),
            TestAI(self.knowledge_base),
            DebuggingAI(self.knowledge_base),
            EnhancerAI(self.knowledge_base),
            DocumentationAI(self.knowledge_base),
            DeploymentAI(self.knowledge_base),
            SecurityAI(self.knowledge_base),
            DatabaseAI(self.knowledge_base),
            LoggingAI(self.knowledge_base),
            VersionControlAI(self.knowledge_base),
            FrontendGeneratorAI(self.knowledge_base)
        ]
    def test_agents_can_handle(self):
        for agent in self.agents:
            self.assertTrue(hasattr(agent, 'can_handle'))
    def test_agents_execute_task(self):
        for agent in self.agents:
            with self.assertRaises(NotImplementedError):
                agent.execute_task('any_task')
    # Add additional tests specific to each agent type
if __name__ == '__main__':
    unittest.main()
