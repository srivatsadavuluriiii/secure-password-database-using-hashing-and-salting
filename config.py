import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # MongoDB Configuration
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    DATABASE_NAME = "user_auth_db"
    COLLECTION_NAME = "users"
    
    # Hashing Configuration - Adjusted for passlib compatibility
    SCRYPT_N = 14  # 2^14 = 16384 - CPU/memory cost parameter (rounds)
    SCRYPT_R = 8      # Block size parameter
    SCRYPT_P = 1      # Parallelization parameter
    
    PBKDF2_ROUNDS = 200000  # Iteration count for PBKDF2