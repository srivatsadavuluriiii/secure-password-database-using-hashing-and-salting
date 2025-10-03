from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, DuplicateKeyError
from config import Config

class DatabaseManager:
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None
        self.connect()
    
    def connect(self):
        try:
            self.client = MongoClient(Config.MONGO_URI)
            self.client.admin.command('ping')
            print("Successfully connected to MongoDB!")
            
            self.db = self.client[Config.DATABASE_NAME]
            self.collection = self.db[Config.COLLECTION_NAME]
        
            self.collection.create_index("email", unique=True)
            print("Database setup completed!")
            
        except ConnectionFailure as e:
            print(f"Could not connect to MongoDB: {e}")
    
    def insert_user(self, user_data):
        try:
            result = self.collection.insert_one(user_data)
            print(f"User inserted with ID: {result.inserted_id}")
            return True
        except DuplicateKeyError:
            print("User with this email already exists!")
            return False
        except Exception as e:
            print(f"Error inserting user: {e}")
            return False
    
    def find_user_by_email(self, email):
        return self.collection.find_one({"email": email})
    
    def close_connection(self):
        if self.client:
            self.client.close()
            print("MongoDB connection closed.")