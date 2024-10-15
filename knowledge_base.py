class SharedKnowledgeBase:
    def __init__(self):
        self.data = {}
        self.task_metadata = {}  # Ensure task_metadata attribute is defined
    
    def store(self, key, value):
        self.data[key] = value
    
    def get(self, key, default=None):
        return self.data.get(key, default)
    
    def delete(self, key):
        if key in self.data:
            del self.data[key]
    
    def list_contents(self):
        """
        Lists all content currently stored in the knowledge base.
        """
        if not self.data:
            print("Shared knowledge base is empty.")
        else:
            print("Shared Knowledge Base Contents:")
            for key, value in self.data.items():
                print(f"  - {key}: {value}")
        return self.data
    
    def store_task_metadata(self, task_name, metadata):
        """
        Stores metadata for a specific task. Metadata can include details such as task difficulty,
        execution time, and success rate.
        """
        if task_name not in self.task_metadata:
            self.task_metadata[task_name] = []
        self.task_metadata[task_name].append(metadata)
        print(f"Stored metadata for task '{task_name}': {metadata}")

    def get_task_metadata(self, task_name):
        """
        Retrieves metadata for a specific task. Returns a list of metadata entries.
        """
        return self.task_metadata.get(task_name, [])

    def list_all_task_metadata(self):
        """
        Lists all metadata stored for tasks.
        """
        if not self.task_metadata:
            print("No task metadata stored.")
        else:
            print("Task Metadata Contents:")
            for task_name, metadata_list in self.task_metadata.items():
                print(f"Task '{task_name}':")
                for metadata in metadata_list:
                    print(f"  - {metadata}")
        return self.task_metadata
