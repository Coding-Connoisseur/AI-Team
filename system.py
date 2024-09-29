from task_priority_queue import TaskPriorityQueue
from task_monitor import TaskMonitor
from agent_health_monitor import AgentHealthMonitor
from system_monitor import SystemMonitor
from health_check_manager import HealthCheckManager
from dynamic_thread_pool import DynamicThreadPoolExecutor
from load_balancer import LoadBalancer

class TeamLeaderAI:
    def __init__(self, agents, retry_limit=3):
        self.agents = agents
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

    def receive_user_input(self, project_overview):
        print(f"Received project: {project_overview}")
        self.decompose_project(project_overview)

    def decompose_project(self, overview):
        tasks = [
            (1, "architecture design"),
            (2, "code generation"),
            (3, "debugging"),
            (4, "testing"),
            (5, "enhancement")
        ]
        for priority, task in tasks:
            self.task_priority_queue.add_task(priority, task)
        self.assign_tasks()

    def assign_tasks(self):
        futures = []
        while self.task_priority_queue.queue:
            task_name = self.task_priority_queue.get_next_task()
            agent = self.load_balancer.assign_task(task_name)
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

    def execute_task(self, agent, task_name):
        result = agent.execute_task(task_name)
        self.task_monitor.end_task(task_name)
        self.agent_health_monitor.record_task(agent.name, result)
        self.health_check_manager.perform_health_check(agent.name)
        self.handle_agent_feedback(task_name, result)

    def handle_agent_feedback(self, task_name, result):
        if result == "success":
            self.task_progress[task_name] = "completed"
        else:
            self.recover_from_failure(task_name)

    def recover_from_failure(self, task):
        if self.task_retries[task] < self.retry_limit:
            self.task_retries[task] += 1
            agent = self.load_balancer.assign_task(task)
            if agent:
                self.execute_task(agent, task)
        else:
            print(f"Task {task} has exceeded the retry limit.")

    def report_progress(self):
        """
        Reports the current progress of tasks.
        """
        print("Task Progress:")
        for task, status in self.task_progress.items():
            print(f"Task: {task}, Status: {status}")
