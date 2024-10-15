from task_priority_queue import TaskPriorityQueue
from task_monitor import TaskMonitor
from agent_health_monitor import AgentHealthMonitor
from system_monitor import SystemMonitor
from health_check_manager import HealthCheckManager
from dynamic_thread_pool import DynamicThreadPoolExecutor
from load_balancer import LoadBalancer, AILoadBalancer
import os
import time

class TeamLeaderAI:
    def __init__(self, agents, retry_limit=3):
        self.agents = agents
        self.task_priority_queue = TaskPriorityQueue(SystemMonitor())  # Using SystemMonitor to help with task scheduling
        self.task_progress = {}  # Track task states: {'task_name': {'status': 'queued/active/completed', 'agent': <agent_name>, 'start_time': <timestamp>}}
        self.task_completion_data = {}  # Track the details of completed tasks
        self.retry_limit = retry_limit
        self.task_retries = {}
        self.thread_pool = DynamicThreadPoolExecutor(max_workers=3)
        #self.load_balancer = LoadBalancer(self.agents.values())  # Reference to LoadBalancer
        self.load_balancer = AILoadBalancer(self.agents.values())
        self.task_monitor = TaskMonitor()  # Task monitor for tracking task execution time
        self.agent_health_monitor = AgentHealthMonitor(self.agents.values(), self.load_balancer)
        self.system_monitor = SystemMonitor()  # Monitor system resources
        self.health_check_manager = HealthCheckManager(self.system_monitor, self.agent_health_monitor)
        self.project_path = None
        self.active_tasks = {}
        self.completed_tasks = []
        self.project_type = []

    def get_user_input(self):
        """
        Asks the user what they want the AI team to do.
        """
        print("What do you want the AI team to do? Choose from the following options:")
        print("1. Create a whole project")
        print("2. Enhance an existing project")
        print("3. Debug a project")
        print("4. Add new features and capabilities to a project")
        print("5. Test a project")
        choice = input("Enter the number of your choice: ")
        return int(choice)
    
    def ask_for_project_path(self):
        """
        Ask the user for the project path and ensure it exists.
        """
        self.project_path = input("Please enter the path to the project you want to work on: ")
        if not os.path.exists(self.project_path):
            print(f"Error: The specified path {self.project_path} does not exist.")
            return False
        return True
    
    def receive_user_input(self):
        """
        Determines what the user wants based on input.
        """
        choice = self.get_user_input()
        if choice == 1:
            print("You selected to create a whole project.")
            self.project_type= input("Enter the type of project (e.g., web app, API, machine learning, etc.): ")
            self.decompose_project(f"Create a {self.project_type}")
        elif choice in [2, 3, 4, 5]:
            if not self.ask_for_project_path():
                return
            if choice == 2:
                print("You selected to enhance an existing project.")
                self.decompose_project("Enhance project")
            elif choice == 3:
                print("You selected to debug a project.")
                self.decompose_project("Debug project")
            elif choice == 4:
                print("You selected to add new features and capabilities.")
                self.decompose_project("Add features and capabilities")
            elif choice == 5:
                print("You selected to test a project.")
                self.decompose_project("Test project")
        else:
            print("Invalid choice.")

    def decompose_project(self, overview):
        tasks = [
            (1, "architecture design"),
            (2, "code generation"),
            (3, "debugging"),
            (4, "testing"),
            (5, "enhancement"),
            (6, "documentation"),
            (7, "deployment"),
            (8, "security audit"),
            (9, "database setup"),
            (10, "logging setup"),
            (11, "version control"),
            (12, "frontend generation")
        ]
        for priority, task in tasks:
            self.task_priority_queue.add_task(priority, task, "medium")
        self.assign_tasks()

    def assign_tasks(self):
        """
        Assign tasks from the task priority queue to agents.
        """
        while task_name := self.task_priority_queue.get_next_task():
            agent = self.load_balancer.assign_task(task_name)
            self.thread_pool.submit_task(self.execute_task, agent, task_name)
            self.update_task_status(task_name, 'active', agent.name)  # Mark task as active
    
    def find_agent_for_task(self, task_name):
        for agent in self.agents.values():
            if agent.can_handle(task_name):
                return agent
        return None
    
    def execute_task(self, agent, task_name):
        """
        Executes the task using the assigned agent.
        """
        try:
            start_time = time.time()  # Track the starting time of the task
            self.task_monitor.start_task(task_name)
            # Execute the task and record its outcome
            outcome = agent.execute_task(task_name)
            elapsed_time = self.task_monitor.end_task(task_name)  # Track task completion time
            self.task_completion_data[task_name] = {
                'status': 'completed',
                'agent': agent.name,
                'duration': elapsed_time,
                'outcome': outcome
            }
            print(f"Task '{task_name}' completed by {agent.name} with outcome: {outcome}")
        except Exception as e:
            print(f"Error in executing task '{task_name}' by {agent.name}: {e}")
            self.record_failure(task_name, agent)

    def handle_agent_feedback(self, task_name, result):
        if result == "success":
            self.task_progress[task_name] = "completed"
        else:
            self.recover_from_failure(task_name)

    def recover_from_failure(self, task):
        if self.task_retries[task] < self.retry_limit:
            self.task_retries[task] += 1
            agent = self.find_agent_for_task(task)
            if agent:
                self.execute_task(agent, task)
        else:
            print(f"Task {task} has exceeded the retry limit.")

    def update_task_status(self, task_name, status, agent_name):
        """
        Updates the task progress status (active, completed, etc.) and records the agent assigned to the task.
        """
        self.task_progress[task_name] = {
            'status': status,
            'agent': agent_name
        }

    def mark_task_completed(self, task_name, agent):
        # Remove from active tasks
        if task_name in self.active_tasks:
            del self.active_tasks[task_name]

        # Add to completed tasks
        self.completed_tasks.append({
            'task': task_name,
            'agent': agent.name,
            'status': 'completed'
        })
        
        # Update dashboard
        self.update_dashboard()

    def report_progress(self):
        """
        Displays a real-time dashboard showing task progress.
        """
        print("\n--- Task Progress Dashboard ---")
        print("Queued Tasks:")
        print("  No queued tasks.")
        print("\nActive Tasks:")
        for task, agent in self.active_tasks.items():
            print(f"  {task} (Agent: {agent.name})")
        
        print("\nCompleted Tasks:")
        if not self.completed_tasks:
            print("  No completed tasks.")
        else:
            for task in self.completed_tasks:
                print(f"  {task['task']} completed by {task['agent']} with status: {task['status']}")
        
        print("--- End of Dashboard Report ---")

    def report_overall_progress(self):
        """
        Summarizes overall task progress, including completion rates.
        """
        total_tasks = len(self.task_progress)
        completed_tasks = len([task for task in self.task_progress if self.task_progress[task]['status'] == 'completed'])
        success_tasks = len([task for task in self.task_completion_data if self.task_completion_data[task]['outcome'] == 'success'])
        print("\n--- Overall Task Completion Summary ---")
        print(f"Total Tasks: {total_tasks}")
        print(f"Completed Tasks: {completed_tasks}")
        print(f"Successful Tasks: {success_tasks}")
        print(f"Completion Rate: {(completed_tasks / total_tasks) * 100:.2f}%")
        print(f"Success Rate: {(success_tasks / completed_tasks) * 100:.2f}% (for completed tasks)")
        print("\n--- End of Summary ---")

    def retry_task(self, task_name, agent_name):
        """
        Attempts to retry a failed task a limited number of times.
        """
        retries = self.task_retries.get(task_name, 0)
        if retries < self.retry_limit:
            print(f"Retrying task '{task_name}' (Attempt {retries + 1}/{self.retry_limit})...")
            self.task_retries[task_name] = retries + 1
            self.assign_tasks()
        else:
            print(f"Task '{task_name}' failed after {self.retry_limit} retries.")

    def record_failure(self, task_name, agent):
        """
        Record task failure and decide whether to retry based on retry limit.
        """
        if task_name not in self.task_retries:
            self.task_retries[task_name] = 0
        if self.task_retries[task_name] < self.retry_limit:
            print(f"Task '{task_name}' failed. Retrying...")
            self.retry_task(task_name, agent.name)
        else:
            print(f"Task '{task_name}' exceeded retry limit. Marked as failed.")
