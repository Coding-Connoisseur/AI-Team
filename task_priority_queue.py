import queue

class TaskPriorityQueue:
    def __init__(self):
        self.queue = queue.PriorityQueue()

    def add_task(self, priority, task_name):
        self.queue.put((priority, task_name))

    def get_next_task(self):
        if not self.queue.empty():
            return self.queue.get()[1]
        return None
