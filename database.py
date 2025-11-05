from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, DuplicateKeyError
from config import Config

class InMemoryCollection:
    def __init__(self):
        self.documents = []
        self.next_id = 1
        self.unique_fields = set()
    
    def create_index(self, field, unique=False):
        if unique:
            self.unique_fields.add(field)
    
    def insert_one(self, document):
        # Check unique constraints
        for field in self.unique_fields:
            if field in document:
                for doc in self.documents:
                    if doc.get(field) == document.get(field):
                        raise DuplicateKeyError(f"Duplicate key error for field {field}")
        
        # Insert document with generated ID
        doc_copy = document.copy()
        doc_copy['_id'] = self.next_id
        self.next_id += 1
        self.documents.append(doc_copy)
        
        class InsertResult:
            def __init__(self, inserted_id):
                self.inserted_id = inserted_id
        
        return InsertResult(doc_copy['_id'])
    
    def find_one(self, filter_dict):
        for doc in self.documents:
            match = True
            for key, value in filter_dict.items():
                if doc.get(key) != value:
                    match = False
                    break
            if match:
                return doc
        return None
    
    def find(self):
        return iter(self.documents)

class DatabaseManager:
    def __init__(self, verbose=True):
        self.client = None
        self.db = None
        self.collection = None
        self.using_fallback = False
        self.connect(verbose=verbose)
    
    def connect(self, verbose=True):
        try:
            self.client = MongoClient(Config.MONGO_URI)
            self.client.admin.command('ping')
            if verbose:
                print("Successfully connected to MongoDB!")
            
            self.db = self.client[Config.DATABASE_NAME]
            self.collection = self.db[Config.COLLECTION_NAME]
        
            self.collection.create_index("email", unique=True)
            if verbose:
                print("Database setup completed!")
            
        except ConnectionFailure as e:
            if verbose:
                print(f"Could not connect to MongoDB: {e}")
                print("Using in-memory fallback storage...")
            self.collection = InMemoryCollection()
            self.collection.create_index("email", unique=True)
            self.using_fallback = True
    
    def insert_user(self, user_data, verbose=True):
        if self.collection is None:
            if verbose:
                print("No database connection available!")
            return False
            
        try:
            result = self.collection.insert_one(user_data)
            if verbose:
                print(f"User inserted with ID: {result.inserted_id}")
                if self.using_fallback:
                    print("(Note: Using in-memory storage, data will be lost on restart)")
            return True
        except DuplicateKeyError:
            if verbose:
                print("User with this email already exists!")
            return False
        except Exception as e:
            if verbose:
                print(f"Error inserting user: {e}")
            return False
    
    def find_user_by_email(self, email):
        if self.collection is None:
            return None
        return self.collection.find_one({"email": email})
    
    def close_connection(self):
        if self.client:
            self.client.close()
            print("MongoDB connection closed.")