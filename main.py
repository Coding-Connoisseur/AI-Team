from system import TeamLeaderAI
from knowledge_base import SharedKnowledgeBase
from agents import (
    ProjectArchitectAI, CodeGeneratorAI, TestAI, EnhancerAI, DocumentationAI,
    DeploymentAI, SecurityAI, DatabaseAI, LoggingAI, VersionControlAI, 
    FrontendGeneratorAI, DebuggingAI
)

# Initialize the shared knowledge base
knowledge_base = SharedKnowledgeBase()

# Define the collaborative agents and pass the shared knowledge base
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

# Initialize the Team Leader AI
team_leader = TeamLeaderAI(agents, knowledge_base)

# Ask the user what they want the team to do
team_leader.receive_user_input()

# Display the progress of task assignments and completions
team_leader.report_progress()

# Example usage of the knowledge base
knowledge_base.store("example_key", "Example knowledge")
print("Knowledge base contents:")
knowledge_base.list_contents()

# Initialize the AI-based Load Balancer with the agent objects only
##load_balancer = AILoadBalancer(agents.values(), knowledge_base)

# Initialize the shared knowledge base instance
#knowledge_base_instance = SharedKnowledgeBase()
