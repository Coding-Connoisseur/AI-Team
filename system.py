from task_priority_queue import TaskPriorityQueue
from task_monitor import TaskMonitor
from agent_health_monitor import AgentHealthMonitor
from system_monitor import SystemMonitor
from health_check_manager import HealthCheckManager
from dynamic_thread_pool import DynamicThreadPoolExecutor
from load_balancer import LoadBalancer
import os
import time

class TeamLeaderAI:
    def __init__(self, agents, knowledge_base, retry_limit=3):
        self.agents = agents
        self.knowledge_base = knowledge_base
        self.task_priority_queue = TaskPriorityQueue(SystemMonitor())
        self.task_progress = {}  # Track task states
        self.task_completion_data = {}  # Track completed task details
        self.retry_limit = retry_limit
        self.task_retries = {}
        self.thread_pool = DynamicThreadPoolExecutor(max_workers=3)
        self.load_balancer = LoadBalancer(self.agents.values(), self.knowledge_base)
        self.task_monitor = TaskMonitor()
        self.agent_health_monitor = AgentHealthMonitor(self.agents.values(), self.load_balancer)
        self.system_monitor = SystemMonitor()
        self.health_check_manager = HealthCheckManager(self.system_monitor, self.agent_health_monitor)
        self.project_path = None
        self.active_tasks = {}
        self.completed_tasks = []
        self.project_type = None

        # Subscribe to task status updates
        for task in self.active_tasks.keys():
            self.knowledge_base.subscribe_to_updates(task, self.on_task_update)

    def get_user_input(self):
        print("What do you want the AI team to do? Choose from the following options:")
        print("1. Create a whole project")
        print("2. Enhance an existing project")
        print("3. Debug a project")
        print("4. Add new features and capabilities to a project")
        print("5. Test a project")
        choice = input("Enter the number of your choice: ")
        return int(choice)

    def ask_for_project_path(self):
        while True:
            path = input("Enter the full path to your project directory: ")
            if os.path.isdir(path):
                return path
            else:
                print("Invalid directory path. Please enter a valid path.")

    def receive_user_input(self):
        choice = self.get_user_input()
        if choice == 1:
            print("You selected to create a whole project.")
            self.project_type = input("Enter the type of project (e.g., web app, API, machine learning, etc.): ")
            self.decompose_project(f"Create a {self.project_type}")
        elif choice in [2, 3, 4, 5]:
            if not self.ask_for_project_path():
                return
            task_overview = {
                2: "Enhance project",
                3: "Debug project",
                4: "Add features and capabilities",
                5: "Test project"
            }
            print(f"You selected to {task_overview[choice].lower()}.")
            self.decompose_project(task_overview[choice])
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
        while task_name := self.task_priority_queue.get_next_task():
            dependencies = self.task_priority_queue.task_dependencies.get(task_name, set())
            if not dependencies:
                agent = self.load_balancer.assign_task(task_name)
                # Pass project_type if required by the agent
                if hasattr(agent, 'execute_task'):
                    self.thread_pool.submit_task(
                        agent.execute_task, task_name, self.project_type if task_name == "architecture design" else None
                    )
                self.update_task_status(task_name, 'active', agent.name)
            else:
                print(f"Task '{task_name}' is waiting for dependencies: {dependencies}")


    def find_agent_for_task(self, task_name):
        for agent in self.agents.values():
            if agent.can_handle(task_name):
                return agent
        return None

    def execute_task(self, agent, task_name):
        try:
            start_time = time.time()
            self.task_monitor.start_task(task_name)
            outcome = agent.execute_task(task_name)
            elapsed_time = self.task_monitor.end_task(task_name)
            self.task_completion_data[task_name] = {
                'status': 'completed',
                'agent': agent.name,
                'duration': elapsed_time,
                'outcome': outcome
            }

            # Mark the task as complete and resolve dependencies
            self.task_priority_queue.mark_task_complete(task_name)
            self.update_task_status(task_name, 'completed', agent.name)
            print(f"Task '{task_name}' completed by {agent.name} with outcome: {outcome}")

        except Exception as e:
            print(f"Error in executing task '{task_name}' by {agent.name}: {e}")
            self.record_failure(task_name, agent)
            self.task_priority_queue.update_task_priority(task_name, priority=0)  # Escalate priority on failure

    def handle_agent_feedback(self, task_name, result):
        if result == "success":
            self.task_progress[task_name] = "completed"
        else:
            self.recover_from_failure(task_name)

    def recover_from_failure(self, task):
        """
        Attempts to retry the task with exponential backoff.

        Args:
            task (str): The task to retry.
        """
        max_delay = 60  # Set a maximum delay to avoid excessively long waits
        base_delay = 1  # Initial delay in seconds

        # Calculate the delay based on the current retry count with exponential backoff
        retries = self.task_retries.get(task, 0)
        delay = min(base_delay * (2 ** retries), max_delay)

        if retries < self.retry_limit:
            self.task_retries[task] = retries + 1
            print(f"Retrying task '{task}' with a delay of {delay} seconds (Attempt {retries + 1}/{self.retry_limit}).")
            time.sleep(delay)  # Apply exponential backoff delay
            agent = self.find_agent_for_task(task)
            if agent:
                self.execute_task(agent, task)
        else:
            print(f"Task '{task}' has exceeded the retry limit after {retries} attempts.")

    def update_task_status(self, task_name, status, agent_name):
        self.task_progress[task_name] = {'status': status, 'agent': agent_name}

    def on_task_update(self, key, value):
        """
        Callback to handle task updates when the status of a task is changed in the knowledge base.

        Args:
            key (str): The task name that was updated.
            value (any): The new value for the task (e.g., completion status).
        """
        print(f"Task '{key}' has been updated with value: {value}")

        # Handle task completion
        if value == 'completed':
            self.mark_task_completed(key)

    def mark_task_completed(self, task_name, agent):
        if task_name in self.active_tasks:
            del self.active_tasks[task_name]
        self.completed_tasks.append({
            'task': task_name,
            'agent': agent.name,
            'status': 'completed'
        })
        self.update_dashboard()

    def report_progress(self):
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
        retries = self.task_retries.get(task_name, 0)
        if retries < self.retry_limit:
            print(f"Retrying task '{task_name}' (Attempt {retries + 1}/{self.retry_limit})...")
            self.task_retries[task_name] = retries + 1
            self.assign_tasks()
        else:
            print(f"Task '{task_name}' failed after {self.retry_limit} retries.")

    def record_failure(self, task_name, agent):
        self.task_retries[task_name] = self.task_retries.get(task_name, 0)
        if self.task_retries[task_name] < self.retry_limit:
            print(f"Task '{task_name}' failed. Retrying...")
            self.retry_task(task_name, agent.name)
        else:
            print(f"Task '{task_name}' exceeded retry limit. Marked as failed.")
