class AgentHealthMonitor:
    """
    Monitors the health and performance of agents.
    """
    def __init__(self, agents, load_balancer):
        self.agent_health = {agent.name: {"tasks_handled": 0, "successes": 0, "failures": 0} for agent in agents}
        self.load_balancer = load_balancer  # Adding load balancer reference to rebalance tasks
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
        self.display_health(agent_name)    # Displaying health after every record.
        self.monitor_agent_health(agent_name)   # Triggering health monitoring after each task
    def display_health(self, agent_name):
        """
        Displays the current health of an agent.
        """
        health = self.agent_health[agent_name]
        print(f"{agent_name} Health: Tasks Handled: {health['tasks_handled']}, Successes: {health['successes']}, Failures: {health['failures']}")
    def monitor_agent_health(self, agent_name):
        """
        Checks if the agent is failing too often and triggers rebalancing if necessary.
        """
        health = self.agent_health[agent_name]
        if health['failures'] > health['successes']:
            print(f"Warning: {agent_name} is experiencing frequent failures.")
            self.trigger_rebalance(agent_name)   # Automatically rebalance if failure rate exceeds success rate.
    def trigger_rebalance(self, failing_agent_name):
        """
        Automatically reassigns tasks if an agent is failing too often.
        """
        print(f"Reassigning tasks from {failing_agent_name} due to frequent failures.")
        # Rebalance logic: Transfer some tasks away from the failing agent to the least busy agent.
        rebalanced_agent = self.load_balancer.assign_task("Rebalance Task")  
        print(f"Tasks reassigned from {failing_agent_name} to {rebalanced_agent.name}.")
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
class HealthCheckManager:
    def __init__(self, system_monitor, agent_health_monitor):
        self.system_monitor = system_monitor
        self.agent_health_monitor = agent_health_monitor
    def perform_health_check(self, agent_name):
        cpu_usage, memory_usage = self.system_monitor.monitor_resources()
        self.agent_health_monitor.monitor_agent_health(agent_name)
        if cpu_usage > 85 or memory_usage > 85:
            print(f"System overload detected. Rebalancing tasks.")
            self.agent_health_monitor.trigger_rebalance(agent_name)
