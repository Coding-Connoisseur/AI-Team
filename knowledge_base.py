import time
import threading

class SharedKnowledgeBase:
    def __init__(self):
        """
        Initializes the knowledge base and task metadata storage.
        `data` stores general key-value pairs with optional expiration.
        `task_metadata` stores task-related information.
        `subscriptions` keeps track of callbacks for key updates.
        `lock` ensures thread-safety when accessing the knowledge base.
        """
        self.data = {}
        self.expiration = {}
        self.task_metadata = {}
        self.subscriptions = {}  # Dictionary to track subscriptions for keys
        self.lock = threading.Lock()

    def store(self, key, value, ttl=None):
        """
        Stores a key-value pair in the knowledge base with an optional time-to-live (TTL).
        Notifies subscribers if the value is updated.

        Args:
            key (str): The key to store the value under.
            value (any): The value to be stored.
            ttl (int): Optional time-to-live in seconds. After TTL, the data will expire.
        """
        with self.lock:
            self.data[key] = value
            if ttl:
                self.expiration[key] = time.time() + ttl
            elif key in self.expiration:
                del self.expiration[key]

            # Notify any subscribers that the key has been updated
            if key in self.subscriptions:
                for callback in self.subscriptions[key]:
                    callback(key, value)

    def get(self, key, default=None):
        """
        Retrieves a value from the knowledge base by key.
        If the key has expired, the data is automatically deleted and default is returned.

        Args:
            key (str): The key whose value needs to be retrieved.
            default (any): The default value to return if the key is not found. Defaults to None.

        Returns:
            any: The value associated with the key, or the default value if the key is not found or expired.
        """
        with self.lock:
            if key in self.expiration and time.time() > self.expiration[key]:
                del self.data[key]
                del self.expiration[key]
                return default
            return self.data.get(key, default)

    def delete(self, key):
        """
        Deletes a key-value pair from the knowledge base.

        Args:
            key (str): The key to be deleted from the knowledge base.
        """
        with self.lock:
            if key in self.data:
                del self.data[key]
            if key in self.expiration:
                del self.expiration[key]

    def list_contents(self):
        """
        Lists all content stored in the knowledge base, excluding expired entries.

        Returns:
            dict: A dictionary containing all valid key-value pairs in the knowledge base.
        """
        with self.lock:
            self._clean_expired()
            if not self.data:
                print("Shared knowledge base is empty.")
            else:
                print("Shared Knowledge Base Contents:")
                for key, value in self.data.items():
                    print(f"  - {key}: {value}")
            return self.data

    def _clean_expired(self):
        """Removes expired entries from the knowledge base."""
        current_time = time.time()
        for key in list(self.expiration.keys()):
            if current_time > self.expiration[key]:
                del self.data[key]
                del self.expiration[key]

    def store_task_metadata(self, task_name, metadata):
        """
        Stores metadata associated with a specific task, such as task performance or duration.
        Automatically aggregates some statistics (e.g., average execution time).

        Args:
            task_name (str): The name of the task.
            metadata (dict): A dictionary containing task-related details (e.g., task difficulty, time taken).
        """
        with self.lock:
            if task_name not in self.task_metadata:
                self.task_metadata[task_name] = {'entries': [], 'stats': {}}
            self.task_metadata[task_name]['entries'].append(metadata)

            # Update aggregated statistics (e.g., average time)
            if 'execution_time' in metadata:
                times = [entry['execution_time'] for entry in self.task_metadata[task_name]['entries'] if 'execution_time' in entry]
                self.task_metadata[task_name]['stats']['average_time'] = sum(times) / len(times)

            print(f"Stored metadata for task '{task_name}': {metadata}")

    def get_task_metadata(self, task_name):
        """
        Retrieves metadata for a specific task, including aggregated statistics.

        Args:
            task_name (str): The name of the task whose metadata is requested.

        Returns:
            dict: A dictionary with both raw metadata entries and aggregated statistics for the task.
        """
        with self.lock:
            return self.task_metadata.get(task_name, {'entries': [], 'stats': {}})

    def list_all_task_metadata(self):
        """
        Lists all metadata stored for tasks, including aggregated statistics.

        Returns:
            dict: A dictionary where the keys are task names and the values contain both raw entries and statistics.
        """
        with self.lock:
            if not self.task_metadata:
                print("No task metadata stored.")
            else:
                print("Task Metadata Contents:")
                for task_name, metadata_info in self.task_metadata.items():
                    print(f"Task '{task_name}':")
                    for metadata in metadata_info['entries']:
                        print(f"  - {metadata}")
                    if 'average_time' in metadata_info['stats']:
                        print(f"  - Average Execution Time: {metadata_info['stats']['average_time']:.2f} seconds")
            return self.task_metadata

    def subscribe_to_updates(self, key, callback):
        """
        Allows an agent to subscribe to updates on a specific key.
        Whenever the key is updated, the provided callback is called.

        Args:
            key (str): The key to subscribe to.
            callback (function): A callback function to call when the key is updated.
        """
        with self.lock:
            if key not in self.subscriptions:
                self.subscriptions[key] = []
            self.subscriptions[key].append(callback)
            print(f"Agent subscribed to updates for key: {key}")

    def unsubscribe_from_updates(self, key, callback):
        """
        Allows an agent to unsubscribe from updates on a specific key.

        Args:
            key (str): The key to unsubscribe from.
            callback (function): The callback function to remove from the subscription list.
        """
        with self.lock:
            if key in self.subscriptions:
                if callback in self.subscriptions[key]:
                    self.subscriptions[key].remove(callback)
                    print(f"Agent unsubscribed from updates for key: {key}")
                if not self.subscriptions[key]:
                    del self.subscriptions[key]
