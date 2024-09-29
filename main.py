from system import TeamLeaderAI
from knowledge_base import SharedKnowledgeBase
from agents import ProjectArchitectAI, CodeGeneratorAI, TestAI, EnhancerAI, DocumentationAI, DeploymentAI, SecurityAI

# Initialize the shared knowledge base
knowledge_base = SharedKnowledgeBase()

# Define collaborative agents and pass the shared knowledge base
agents = {
    "Project Architect AI": ProjectArchitectAI(knowledge_base),
    "Code Generator AI": CodeGeneratorAI(knowledge_base),
    "Test AI": TestAI(knowledge_base),
    "Enhancer AI": EnhancerAI(knowledge_base)
}

# Initialize the Team Leader AI
team_leader = TeamLeaderAI(agents)

# Sample user input to start the project
team_leader.receive_user_input("Build a large-scale web application.")
team_leader.report_progress()

# Print the contents of the knowledge base
knowledge_base.list_contents()
