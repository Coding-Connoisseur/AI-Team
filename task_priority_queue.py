import heapq

class TaskPriorityQueue:
    def __init__(self):
        self.queue = []

    def add_task(self, priority, task_name):
        heapq.heappush(self.queue, (priority, task_name))

    def get_next_task(self):
        if self.queue:
            return heapq.heappop(self.queue)[1]
        return None
