class AgentHealthMonitor:
    """
    Monitors the health and performance of agents.
    """
    def __init__(self, agents):
        self.agent_health = {agent.name: {"tasks_handled": 0, "successes": 0, "failures": 0} for agent in agents}
    
    def record_task(self, agent_name, outcome):
        """
        Records the outcome of a task handled by an agent.
        Expects 'outcome' to be either 'success' or 'failure' and updates the agent's health accordingly.
        """
        self.agent_health[agent_name]["tasks_handled"] += 1
        
        if outcome == "success":
            self.agent_health[agent_name]["successes"] += 1
        elif outcome == "failure":
            self.agent_health[agent_name]["failures"] += 1
        else:
            raise ValueError(f"Unknown task outcome: {outcome}")

        self.display_health(agent_name)

    def display_health(self, agent_name):
        """
        Displays the current health of an agent.
        """
        health = self.agent_health[agent_name]
        print(f"{agent_name} Health: Tasks Handled: {health['tasks_handled']}, Successes: {health['successes']}, Failures: {health['failures']}")

    def monitor_agent_health(self, agent_name):
        """
        Checks if the agent is failing too often and triggers alerts if necessary.
        """
        health = self.agent_health[agent_name]
        if health['failures'] > health['successes']:
            print(f"Warning: {agent_name} is experiencing frequent failures.")
