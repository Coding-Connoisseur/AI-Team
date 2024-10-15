from sklearn.tree import DecisionTreeRegressor
import numpy as np
import psutil

class LoadBalancer:
    """
    Distributes tasks evenly across available agents to avoid bottlenecks.
    Now considers agent expertise when assigning tasks.
    """
    def __init__(self, agents):
        self.agents = agents
        self.agent_loads = {agent.name: 0 for agent in agents}
        self.agent_expertises = {  # Identifying the best agent for each type of task
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
    def assign_task(self, task):
        """
        Assigns the task to the least busy agent, while also prioritizing agents who are experts at this task.
        """
        # Identify the expert agent for the task
        expert_agent_name = self.agent_expertises.get(task)
        if expert_agent_name:
            # Ensure the expert agent still exists in the system
            if expert_agent_name in self.agent_loads:
                least_busy_expert = expert_agent_name
            else:
                # Fallback to least busy agent if expertise agent is not found
                least_busy_expert = min(self.agent_loads, key=self.agent_loads.get)
            print(f"Assigning task '{task}' to the expert agent: {least_busy_expert}.")
        else:
            # No specific expertise available, assign to the least busy agent
            least_busy_expert = min(self.agent_loads, key=self.agent_loads.get)
            print(f"Assigning task '{task}' to {least_busy_expert}, no specific expertise required.")
        assigned_agent = next(agent for agent in self.agents if agent.name == least_busy_expert)
        self.agent_loads[least_busy_expert] += 1
        return assigned_agent
    def task_completed(self, agent_name):
        """
        Marks a task as completed by the given agent, reducing their current load.
        """
        if agent_name in self.agent_loads:
            self.agent_loads[agent_name] = max(0, self.agent_loads[agent_name] - 1)
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
    def __init__(self, agents):
        super().__init__(agents)
        self.data_log = []  # Collect data for training
        self.model = DecisionTreeRegressor()  # Initialize a simple predictive model

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

