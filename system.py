from task_priority_queue import TaskPriorityQueue
from task_monitor import TaskMonitor
from agent_health_monitor import AgentHealthMonitor
from system_monitor import SystemMonitor
from health_check_manager import HealthCheckManager
from dynamic_thread_pool import DynamicThreadPoolExecutor
from load_balancer import LoadBalancer
import os

class TeamLeaderAI:
    def __init__(self, agents, knowledge_base, retry_limit=3):
        self.agents = agents
        self.knowledge_base = knowledge_base
        self.task_priority_queue = TaskPriorityQueue()
        self.task_progress = {}
        self.retry_limit = retry_limit
        self.task_retries = {}
        self.thread_pool = DynamicThreadPoolExecutor(max_workers=3)
        self.load_balancer = LoadBalancer(self.agents.values())
        self.task_monitor = TaskMonitor()
        self.agent_health_monitor = AgentHealthMonitor(self.agents.values())
        self.system_monitor = SystemMonitor()
        self.health_check_manager = HealthCheckManager(self.system_monitor, self.agent_health_monitor)
        self.project_path = None

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
        
        while True:
            choice = input("Enter the number of your choice: ")
            try:
                # Convert input to integer
                choice = int(choice)
                # Check if the choice is within valid range
                if choice in [1, 2, 3, 4, 5]:
                    return choice
                else:
                    print("Invalid choice. Please select a number between 1 and 5.")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 5.")

    def ask_for_project_path(self):
        """
        Ask the user for the project path and ensure it exists.
        """
        while True:
            self.project_path = input("Please enter the path to the project you want to work on: ")
            if os.path.exists(self.project_path):
                self.knowledge_base.store("project_structure", self.project_path)
                return True
            else:
                print(f"Error: The specified path {self.project_path} does not exist. Please enter a valid path.")

    def receive_user_input(self):
        """
        Determines what the user wants based on input and proceeds accordingly.
        """
        choice = self.get_user_input()
        if choice == 1:
            print("You selected to create a whole project.")
            project_type = input("Enter the type of project (e.g., web app, API, machine learning, etc.): ")
            self.decompose_project(f"Create a {project_type}")
        elif choice in [2, 3, 4, 5]:
            if self.ask_for_project_path():
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
        """
        Breaks down the project into tasks and adds them to the priority queue.
        """
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
            self.task_priority_queue.add_task(priority, task)
        self.assign_tasks()

    def assign_tasks(self):
        """
        Assigns tasks to available agents and manages task execution.
        """
        futures = []
        while self.task_priority_queue.queue:
            task_name = self.task_priority_queue.get_next_task()
            agent = self.find_agent_for_task(task_name)
            if agent:
                print(f"Assigning {task_name} to {agent.name}")
                self.task_progress[task_name] = "in progress"
                self.task_retries[task_name] = 0
                self.task_monitor.start_task(task_name)
                futures.append(self.thread_pool.submit_task(self.execute_task, agent, task_name))
            else:
                print(f"No agent available for task: {task_name}")
                self.task_progress[task_name] = "unassigned"

        for future in futures:
            future.result()

    def find_agent_for_task(self, task_name):
        """
        Finds an available agent that can handle the given task.
        """
        for agent in self.agents.values():
            if agent.can_handle(task_name):
                return agent
        return None

    def execute_task(self, agent, task_name):
        """
        Executes the assigned task and handles the result.
        """
        result = agent.execute_task(task_name)
        self.task_monitor.end_task(task_name)
        self.agent_health_monitor.record_task(agent.name, result)
        self.health_check_manager.perform_health_check(agent.name)
        self.handle_agent_feedback(task_name, result)

    def handle_agent_feedback(self, task_name, result):
        """
        Handles feedback from agents based on task result.
        """
        if result == "success":
            self.task_progress[task_name] = "completed"
        else:
            self.recover_from_failure(task_name)

    def recover_from_failure(self, task_name):
        """
        Attempts to recover from task failure by retrying the task, within limits.
        """
        if self.task_retries[task_name] < self.retry_limit:
            self.task_retries[task_name] += 1
            agent = self.find_agent_for_task(task_name)
            if agent:
                self.execute_task(agent, task_name)
        else:
            print(f"Task {task_name} has exceeded the retry limit.")

    def report_progress(self):
        """
        Reports the progress of all tasks.
        """
        print("Task Progress:")
        for task, status in self.task_progress.items():
            print(f"Task: {task}, Status: {status}")
