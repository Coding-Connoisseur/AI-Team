from concurrent.futures import ThreadPoolExecutor

class DynamicThreadPoolExecutor:
    def __init__(self, max_workers):
        self.max_workers = max_workers
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def adjust_workers(self, cpu_usage, memory_usage):
        if cpu_usage > 80 or memory_usage > 80:
            new_worker_count = max(1, self.max_workers // 2)
            self.executor = ThreadPoolExecutor(max_workers=new_worker_count)
        elif cpu_usage < 40 and memory_usage < 40:
            new_worker_count = min(self.max_workers * 2, 10)
            self.executor = ThreadPoolExecutor(max_workers=new_worker_count)

    def submit_task(self, fn, *args, **kwargs):
        return self.executor.submit(fn, *args, **kwargs)
