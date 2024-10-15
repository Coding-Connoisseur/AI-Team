import psutil
from concurrent.futures import ThreadPoolExecutor
class DynamicThreadPoolExecutor:
    def __init__(self, max_workers):
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    def adjust_workers(self, cpu_usage, memory_usage, io_usage, network_usage):
        """
        Adjust worker count based on system's resource usage, including disk I/O and network bandwidth.
        """
        # Reduce the number of workers if CPU, memory, disk I/O, or network usage is too high
        if cpu_usage > 80 or memory_usage > 80 or io_usage > 80 or network_usage > 75:
            new_worker_count = max(1, self.max_workers // 2)  # Reduce workers to alleviate load
            self.executor = ThreadPoolExecutor(max_workers=new_worker_count)
            print(f"Reducing worker count to {new_worker_count} due to high resource usage: CPU({cpu_usage}%), Memory({memory_usage}%), IO({io_usage}%), Network({network_usage}%)")
        # Increase workers if the system is underutilized
        elif cpu_usage < 40 and memory_usage < 40 and io_usage < 40 and network_usage < 30:
            new_worker_count = min(self.max_workers * 2, 10)  # Increase workers to better utilize capacity
            self.executor = ThreadPoolExecutor(max_workers=new_worker_count)
            print(f"Increasing worker count to {new_worker_count} due to low resource usage: CPU({cpu_usage}%), Memory({memory_usage}%), IO({io_usage}%), Network({network_usage}%)")
    def monitor_resource_usage(self):
        """
        Fetch system resource usage: CPU, memory, disk I/O, and network IO.
        """
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent
        io_usage = psutil.disk_io_counters().write_time   # Monitoring disk write time in milliseconds
        network_usage = psutil.net_io_counters().bytes_sent  # Monitoring network bytes sent
        # Normalize IO and network data
        normalized_io_usage = min(100, (io_usage / 1000) * 10)  # Simple normalization (adjust as necessary)
        normalized_network_usage = min(100, (network_usage / (1024 * 1024)) * 10)  # Convert bytes to MB and normalize
        return cpu_usage, memory_usage, normalized_io_usage, normalized_network_usage
    def submit_task(self, fn, *args, **kwargs):
        """
        Submit a task to the executor, dynamically adjusting the worker count based on system resources.
        """
        cpu_usage, memory_usage, io_usage, network_usage = self.monitor_resource_usage()
        self.adjust_workers(cpu_usage, memory_usage, io_usage, network_usage)
        return self.executor.submit(fn, *args, **kwargs)
