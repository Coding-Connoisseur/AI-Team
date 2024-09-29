import psutil

class SystemMonitor:
    def monitor_resources(self):
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent
        print(f"CPU Usage: {cpu_usage}%, Memory Usage: {memory_usage}%")
        return cpu_usage, memory_usage
