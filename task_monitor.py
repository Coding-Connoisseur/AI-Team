import time

class TaskMonitor:
    def __init__(self):
        self.task_times = {}

    def start_task(self, task_name):
        self.task_times[task_name] = time.time()

    def end_task(self, task_name):
        if task_name in self.task_times:
            elapsed_time = time.time() - self.task_times[task_name]
            print(f"Task '{task_name}' completed in {elapsed_time:.2f} seconds.")
            del self.task_times[task_name]
            return elapsed_time
        return None
