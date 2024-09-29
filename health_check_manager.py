class HealthCheckManager:
    def __init__(self, system_monitor, agent_health_monitor):
        self.system_monitor = system_monitor
        self.agent_health_monitor = agent_health_monitor

    def perform_health_check(self, agent_name):
        cpu_usage, memory_usage = self.system_monitor.monitor_resources()
        self.agent_health_monitor.monitor_agent_health(agent_name)
        if cpu_usage > 85 or memory_usage > 85:
            print(f"System overload detected. Rebalancing tasks.")
