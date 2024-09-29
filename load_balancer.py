class LoadBalancer:
    """
    Distributes tasks evenly across available agents to avoid bottlenecks.
    """
    def __init__(self, agents):
        self.agents = agents
        self.agent_loads = {agent.name: 0 for agent in agents}

    def assign_task(self, task):
        """
        Assigns the task to the least busy agent.
        """
        least_busy_agent = min(self.agent_loads, key=self.agent_loads.get)
        print(f"Assigning task '{task}' to {least_busy_agent}.")
        return [agent for agent in self.agents if agent.name == least_busy_agent][0]

    def task_completed(self, agent_name):
        """
        Marks a task as completed by the given agent.
        """
        self.agent_loads[agent_name] -= 1
