class SharedKnowledgeBase:
    def __init__(self):
        self.storage = {}
    
    def store(self, key, value):
        self.storage[key] = value
        print(f"Knowledge Base: Stored {key}")
    
    def retrieve(self, key):
        return self.storage.get(key, None)
    
    def list_contents(self):
        print("Knowledge Base Contents:")
        for key, value in self.storage.items():
            print(f"{key}: {value}")
