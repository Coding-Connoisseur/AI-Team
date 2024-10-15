from system import TeamLeaderAI
from knowledge_base import SharedKnowledgeBase
from agents import ProjectArchitectAI, CodeGeneratorAI, TestAI, EnhancerAI, DocumentationAI, DeploymentAI, SecurityAI, DatabaseAI, LoggingAI, VersionControlAI, FrontendGeneratorAI, DebuggingAI
from load_balancer import AILoadBalancer, LoadBalancer

# Initialize the shared knowledge base
knowledge_base = SharedKnowledgeBase()

# Define collaborative agents and pass the shared knowledge base
agents = {
    "Project Architect AI": ProjectArchitectAI(knowledge_base),
    "Code Generator AI": CodeGeneratorAI(knowledge_base),
    "Test AI": TestAI(knowledge_base),
    "Enhancer AI": EnhancerAI(knowledge_base),
    "Documentation AI": DocumentationAI(knowledge_base),
    "Deployment AI": DeploymentAI(knowledge_base),
    "Security AI": SecurityAI(knowledge_base),
    "Database AI": DatabaseAI(knowledge_base),
    "Logging AI": LoggingAI(knowledge_base),
    "Version Control AI": VersionControlAI(knowledge_base),
    "Frontend Generator AI": FrontendGeneratorAI(knowledge_base),
    "Debugging AI": DebuggingAI(knowledge_base)
}
# Initialize the AI-based Load Balancer
# Initialize the AI-based Load Balancer with the agent objects only
load_balancer = AILoadBalancer(agents.values())

# Initialize the Team Leader AI
team_leader = TeamLeaderAI(agents)

# Ask the user what they want the team to do
team_leader.receive_user_input()
# Print the task progress
team_leader.report_progress()

# Store some knowledge in the knowledge base
knowledge_base.store("key1", "This is some knowledge about task1.")
knowledge_base.store("key2", "This is some knowledge about task2.")
# List the shared knowledge base contents:
knowledge_base.list_contents()

# Retrieve specific knowledge
task1_knowledge = knowledge_base.get("key1")
print(f"Retrieved knowledge for task1: {task1_knowledge}")
task2_knowledge = knowledge_base.get("key2")
print(f"Retrieved knowledge for task2: {task2_knowledge}")
