class AgentHealthMonitor:
    def __init__(self, agents):
        self.agent_health = {agent.name: {"successes": 0, "failures": 0} for agent in agents}

    def record_task(self, agent_name, outcome):
        self.agent_health[agent_name][outcome] += 1
        self.display_health(agent_name)

    def display_health(self, agent_name):
        health = self.agent_health[agent_name]
        print(f"{agent_name} Health: Successes: {health['successes']}, Failures: {health['failures']}")
