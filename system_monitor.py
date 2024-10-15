import psutil
class SystemMonitor:
    def __init__(self):
        self.alert_thresholds = {
            'cpu': 85,  # Alert if CPU usage exceeds 85%
            'memory': 85,  # Alert if memory usage exceeds 85%
            'disk': 80,  # Alert if disk usage exceeds 80%
            'network_sent': 75,  # Alert if network outgoing exceeds 75% of bandwidth (mock)
        }
    def monitor_resources(self):
        """
        Monitors the system's resource usage.
        """
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        network_usage_sent = self.get_network_sent_usage()
        print(f"CPU Usage: {cpu_usage}%, Memory Usage: {memory_usage}%, Disk Usage: {disk_usage}%, Network Outgoing: {network_usage_sent}%")
        # Trigger alerts if any usage exceeds pre-defined thresholds
        self.check_alerts(cpu_usage, memory_usage, disk_usage, network_usage_sent)
        return cpu_usage, memory_usage, disk_usage, network_usage_sent
    def check_alerts(self, cpu_usage, memory_usage, disk_usage, network_usage_sent):
        """
        Checks system metrics against pre-defined threshold limits and issues alerts if exceeded.
        """
        if cpu_usage > self.alert_thresholds['cpu']:
            print(f"ALERT: CPU Usage exceeds {self.alert_thresholds['cpu']}% (Current: {cpu_usage}%)")
        if memory_usage > self.alert_thresholds['memory']:
            print(f"ALERT: Memory Usage exceeds {self.alert_thresholds['memory']}% (Current: {memory_usage}%)")
        if disk_usage > self.alert_thresholds['disk']:
            print(f"ALERT: Disk Usage exceeds {self.alert_thresholds['disk']}% (Current: {disk_usage}%)")
        if network_usage_sent > self.alert_thresholds['network_sent']:
            print(f"ALERT: Network Outgoing exceeds {self.alert_thresholds['network_sent']}% (Current: {network_usage_sent}%)")
    def get_network_sent_usage(self):
        """
        Simulate network usage monitoring. You could modify this part to reflect real network usage.
        """
        net_io = psutil.net_io_counters()
        sent = net_io.bytes_sent / (1024 * 1024)  # Convert the sent bytes to megabytes
        # For now, we'll return a mock "percentage", just scale bytes sent arbitrarily
        return min(100, (sent / 5) * 10)  # This is a mock calculation assuming 5MB threshold.
    def trigger_alert(self, alert_message):
        """
        Optional: Hook this up with a notification/alerting system (e.g., email, logging, etc.).
        """
        # Notifies via print for now; can change as needed (e.g., hook with logging service).
        print(f"Triggering Alert: {alert_message}")
