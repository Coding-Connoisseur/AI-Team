import heapq
class TaskPriorityQueue:
    def __init__(self, system_monitor):
        self.queue = []
        self.system_monitor = system_monitor  # Allow access to system resource data
    def add_task(self, priority, task_name, resource_intensity):
        """
        Add task to priority queue with priority and an estimated resource intensity (e.g., high, medium, low).
        """
        heapq.heappush(self.queue, (priority, task_name, resource_intensity))
    def get_next_task(self):
        """
        Fetch the next task, prioritizing based on system resource availability.
        """
        if not self.queue:
            return None
        # Get system's current resources utilization
        cpu_usage, memory_usage, _, _ = self.system_monitor.monitor_resources()
        # Try to prioritize tasks that match the current system conditions
        best_match = None
        for i in range(len(self.queue)):
            priority, task_name, resource_intensity = self.queue[i]
            if resource_intensity == 'low' or (cpu_usage < 50 and memory_usage < 50):
                best_match = heapq.heappop(self.queue)
                break
            elif resource_intensity == 'medium' and (cpu_usage < 70 and memory_usage < 70):
                best_match = heapq.heappop(self.queue)
                break
            elif resource_intensity == 'high' and (cpu_usage < 90 and memory_usage < 90):
                best_match = heapq.heappop(self.queue)
                break
        if best_match:
            return best_match[1]  # Return the task_name after finding the best match
        else:
            print("System is too overloaded; delaying resource-heavy tasks.")
            return None
    def display_pending_tasks(self):
        """
        Display tasks currently pending in the queue, sorted by priority.
        """
        if not self.queue:
            print("No pending tasks.")
            return
        print("Pending tasks:")
        for priority, task_name, resource_intensity in sorted(self.queue):
            print(f"Priority {priority}: Task '{task_name}' (Resource Intensity: {resource_intensity})")
