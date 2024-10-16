from sklearn.tree import DecisionTreeRegressor
import numpy as np
import psutil
from knowledge_base import SharedKnowledgeBase
import knowledge_base

class LoadBalancer:
    def __init__(self, agents, knowledge_base):
        self.agents = agents
        self.knowledge_base = knowledge_base
        self.agent_loads = {agent.name: 0 for agent in agents}
        self.agent_expertises = {
            "architecture design": "Project Architect AI",
            "code generation": "Code Generator AI",
            "debugging": "Debugging AI",
            "testing": "Test AI",
            "enhancement": "Enhancer AI",
            "documentation": "Documentation AI",
            "deployment": "Deployment AI",
            "security audit": "Security AI",
            "database setup": "Database AI",
            "logging setup": "Logging AI",
            "version control": "Version Control AI",
            "frontend generation": "Frontend Generator AI"
        }

    def assign_task(self, task_name):
        """
        Assigns a task to the least busy or most specialized agent.
        
        Args:
            task_name (str): The name of the task to assign.
        
        Returns:
            The selected agent for the task.
        """
        expert_agent_name = self.agent_expertises.get(task_name)
        if expert_agent_name:
            least_busy_agent = min(self.agent_loads, key=self.agent_loads.get)
            assigned_agent = next((agent for agent in self.agents if agent.name == expert_agent_name), None)
            if assigned_agent:
                print(f"Assigned {task_name} to specialized agent: {assigned_agent.name}")
            else:
                assigned_agent = next(agent for agent in self.agents if agent.name == least_busy_agent)
                print(f"Assigned {task_name} to least busy agent: {assigned_agent.name}")
        else:
            assigned_agent = next(agent for agent in self.agents if agent.name == min(self.agent_loads, key=self.agent_loads.get))
            print(f"Assigned {task_name} to least busy agent: {assigned_agent.name}")
        
        self.agent_loads[assigned_agent.name] += 1
        return assigned_agent

    def estimate_task_duration(self, task_name):
        """
        Estimates the duration of a task based on past task completion times.
        
        Args:
            task_name (str): The name of the task to estimate.
        
        Returns:
            float: The estimated duration in seconds, or None if there is no data.
        """
        task_metadata = self.knowledge_base.get_task_metadata(task_name)
        
        if task_metadata:
            total_time = sum(entry['duration'] for entry in task_metadata)
            average_duration = total_time / len(task_metadata)
            print(f"Estimated duration for task '{task_name}': {average_duration:.2f} seconds.")
            return average_duration
        else:
            print(f"No historical data available to estimate duration for task '{task_name}'.")
            return None

    def task_completed(self, agent_name):
        """
        Marks a task as completed for an agent, reducing their current load.
        
        Args:
            agent_name (str): The name of the agent who completed a task.
        """
        if agent_name in self.agent_loads:
            self.agent_loads[agent_name] = max(0, self.agent_loads[agent_name] - 1)
            print(f"Marked task completed for agent: {agent_name}")

# Example agents list to simulate load balancer functioning:
"""
agents = {
    "Project Architect AI": ProjectArchitectAI(knowledge_base),
    "Code Generator AI": CodeGeneratorAI(knowledge_base),
    "Debugging AI": DebuggingAI(knowledge_base),
    "Test AI": TestAI(knowledge_base),
    "Enhancer AI": EnhancerAI(knowledge_base),
    "Documentation AI": DocumentationAI(knowledge_base),
    "Deployment AI": DeploymentAI(knowledge_base),
    "Security AI": SecurityAI(knowledge_base),
    "Database AI": DatabaseAI(knowledge_base),
    "Logging AI": LoggingAI(knowledge_base),
    "Version Control AI": VersionControlAI(knowledge_base),
    "Frontend Generator AI": FrontendGeneratorAI(knowledge_base)
}
"""

class AILoadBalancer(LoadBalancer):
    def __init__(self, agents, knowledge_base):
        super().__init__(agents)
        self.data_log = []  # Collect data for training
        self.model = DecisionTreeRegressor()  # Initialize a simple predictive model        
        knowledge_base_instance = SharedKnowledgeBase()

    def monitor_resource_usage(self):
        # Use psutil to get system resource usage
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        net_io = psutil.net_io_counters()
        network_outgoing = net_io.bytes_sent / 1024 / 1024  # Convert to MB
        return cpu_usage, memory_usage, disk_usage, network_outgoing
    
    def collect_data(self, task_name, agent_name, cpu_usage, memory_usage, task_duration, success):
        # Log data points for training
        self.data_log.append([cpu_usage, memory_usage, task_duration, int(success)])
        # Keep log size manageable
        if len(self.data_log) > 1000:
            self.data_log.pop(0)

    def train_model(self):
        # Train model with collected data if there are enough samples
        if len(self.data_log) >= 50:
            X = np.array(self.data_log)[:, :3]  # cpu, memory, task duration
            y = np.array(self.data_log)[:, 3]  # success rate
            self.model.fit(X, y)

    def estimate_task_duration(self, task_name):
        """
        Estimates the duration of a task based on past task completion times.

        Args:
            task_name (str): The name of the task to estimate. This parameter is a string representing the name of the task.

        Returns:
            float: The estimated duration in seconds, or None if there is no data. The function returns a float value representing the estimated duration of the task in seconds. If no historical data is available, it returns None.
        """
        # Retrieve task metadata from the knowledge base
        task_metadata = self.knowledge_base.get_task_metadata(task_name)

        # Calculate average duration if metadata is available
        if task_metadata:
            total_time = sum(entry['duration'] for entry in task_metadata)
            average_duration = total_time / len(task_metadata)
            print(f"Estimated duration for task '{task_name}': {average_duration:.2f} seconds.")
            return average_duration
        else:
            print(f"No historical data available to estimate duration for task '{task_name}'.")
            return None

    def assign_task(self, task):
        # Monitor system and predict optimal assignment
        cpu_usage, memory_usage, _, _ = self.monitor_resource_usage()
        task_duration = self.estimate_task_duration(task)  # Placeholder function
        self.train_model()
        
        prediction = self.model.predict([[cpu_usage, memory_usage, task_duration]])
        optimal_agent_name = self.find_optimal_agent(prediction)  # Placeholder for finding agent based on model
        
        # Use prediction to assign task
        if optimal_agent_name:
            assigned_agent = next(agent for agent in self.agents if agent.name == optimal_agent_name)
            print(f"AI LoadBalancer assigned task '{task}' to agent '{optimal_agent_name}'")
            return assigned_agent
        else:
            return super().assign_task(task)  # Fallback to standard method if no optimal agent is found

