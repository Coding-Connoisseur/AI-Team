import heapq
import numpy as np
from sklearn.linear_model import LinearRegression

class TaskPriorityQueue:
    def __init__(self, system_monitor):
        self.queue = []
        self.system_monitor = system_monitor  # Allow access to system resource data
        self.tasks = []  # This will hold our priority queue (min-heap)
        self.task_dependencies = {}  # Track task dependencies
        self.task_data = []  # Initialize task_data for AI training
        self.model = LinearRegression()  # Model for task priority prediction

    def add_task(self, priority, task_name, priority_level, dependencies=[]):
        """
        Adds a task to the priority queue with AI-adjusted priority and optional dependencies.
        
        Args:
            priority (int): The initial priority of the task (lower number = higher priority).
            task_name (str): The name of the task to add.
            priority_level (str): Task priority level, like 'high', 'medium', or 'low'.
            dependencies (list): List of task names that must be completed before this task starts.
        """
        # Check if the model is ready to make predictions (i.e., has been trained with enough data)
        if len(self.task_data) > 50:
            # Predict an adjusted priority based on AI model
            adjusted_priority = self.model.predict([[priority]])[0]
            print(f"AI adjusted priority for '{task_name}' from {priority} to {adjusted_priority}.")
        else:
            # Fallback to the original priority if not enough data
            adjusted_priority = priority

        # Add the task with the adjusted priority to the queue
        heapq.heappush(self.tasks, (adjusted_priority, task_name, priority_level))
        
        # Log dependencies
        if dependencies:
            self.task_dependencies[task_name] = set(dependencies)

        print(f"Task '{task_name}' added with priority {adjusted_priority} and dependencies: {dependencies}")
        
        # Log task data to improve future predictions
        self.log_task_data(priority, task_name, priority_level)


    def get_next_task(self):
        """
        Retrieves the next available task based on priority and dependencies.
        """
        for i, (priority, task_name, priority_level) in enumerate(self.tasks):
            if task_name not in self.task_dependencies:
                return heapq.heappop(self.tasks)[1]  # Return task name without dependencies

            # Check if dependencies are completed
            if all(dep not in self.task_dependencies for dep in self.task_dependencies[task_name]):
                # Remove dependencies and task from queue
                del self.task_dependencies[task_name]
                return heapq.heappop(self.tasks)[1]

        print("No tasks available due to unresolved dependencies.")
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

    def log_task_data(self, priority, task_name, priority_level):
        """
        Logs task data for training the AI model.
        
        Args:
            priority (int): The initial priority of the task.
            task_name (str): The name of the task to add.
            priority_level (str): Task priority level, like 'high', 'medium', or 'low'.
        """
        task_features = [priority]  # Feature vector can be expanded as needed
        self.task_data.append((task_features, priority_level))

        # Train the model with new data if enough samples are collected
        if len(self.task_data) > 50:
            X, y = zip(*self.task_data)
            self.model.fit(X, y)
            print("AI model for task priority has been updated with new data.")
            
    def update_task_priority(self, task_name, new_priority):
        """
        Updates the priority of a specific task.
        """
        # Find and remove the task to update its priority
        for i, (priority, name, level) in enumerate(self.tasks):
            if name == task_name:
                self.tasks.pop(i)
                heapq.heapify(self.tasks)  # Rebalance the heap
                self.add_task(new_priority, task_name, level)
                print(f"Updated priority for task '{task_name}' to {new_priority}.")
                return
        print(f"Task '{task_name}' not found in the queue.")

    def mark_task_complete(self, task_name):
        """
        Removes a completed task from the dependencies of other tasks.
        """
        for task, dependencies in self.task_dependencies.items():
            if task_name in dependencies:
                dependencies.remove(task_name)
                print(f"Task '{task_name}' dependency removed from '{task}'.")
        # Remove the task if it's no longer a dependency
        if task_name in self.task_dependencies:
            del self.task_dependencies[task_name]
        print(f"Marked task '{task_name}' as complete and resolved dependencies.")
