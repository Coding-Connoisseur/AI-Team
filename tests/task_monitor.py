import time
class TaskMonitor:
    def __init__(self):
        self.task_times = {}
        self.task_history = {}  # New dictionary to track task completion times
    def start_task(self, task_name):
        """
        Starts tracking the task's start time.
        """
        self.task_times[task_name] = time.time()
        print(f"Started task '{task_name}' at {self.task_times[task_name]}")
    def end_task(self, task_name):
        """
        Stops tracking the task's time and records the duration for analytics.
        """
        if task_name in self.task_times:
            elapsed_time = time.time() - self.task_times[task_name]
            print(f"Task '{task_name}' completed in {elapsed_time:.2f} seconds.")
            # Store the elapsed time in task history for tracking multiple runs
            if task_name not in self.task_history:
                self.task_history[task_name] = []
            self.task_history[task_name].append(elapsed_time)
            del self.task_times[task_name]
            return elapsed_time
        return None
    def get_average_time(self, task_name):
        """
        Calculates the average completion time for a given task, based on historical data.
        """
        if task_name in self.task_history and self.task_history[task_name]:
            avg_time = sum(self.task_history[task_name]) / len(self.task_history[task_name])
            print(f"Average time for task '{task_name}': {avg_time:.2f} seconds.")
            return avg_time
        else:
            print(f"No historical data for task '{task_name}'.")
            return None
    def display_task_statistics(self):
        """
        Displays a summary of task performance statistics, including average and total run times.
        """
        if self.task_history:
            print("\nTask Performance Summary:")
            for task_name, times in self.task_history.items():
                total_runs = len(times)
                total_time = sum(times)
                average_time = total_time / total_runs if total_runs > 0 else 0
                print(f"Task: {task_name}, Total Runs: {total_runs}, Average Time: {average_time:.2f} seconds, Total Time: {total_time:.2f} seconds.")
        else:
            print("No tasks have been completed yet to show statistics.")
