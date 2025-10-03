from datetime import datetime
from database import DatabaseManager
from auth_manager import AuthManager
import getpass

class AuthApp:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.auth_manager = AuthManager()
    
    def register_user(self):
        print("\n--- User Registration ---")
        email = input("Enter email: ").strip().lower()
        password = getpass.getpass("Enter password: ")
        confirm_password = getpass.getpass("Confirm password: ")
        
        if password != confirm_password:
            print("Passwords don't match!")
            return
        
        algorithm = input("Choose algorithm (scrypt/pbkdf2) [default: scrypt]: ").strip().lower()
        if algorithm not in ['scrypt', 'pbkdf2']:
            algorithm = 'scrypt'
        
        try:
            user_data = self.auth_manager.create_user_data(email, password, algorithm)
            
            if self.db_manager.insert_user(user_data):
                print("User registered successfully!")
            else:
                print("Failed to register user.")
                
        except Exception as e:
            print(f"Error during registration: {e}")
    
    def login_user(self):
        print("\n--- User Login ---")
        email = input("Enter email: ").strip().lower()
        password = getpass.getpass("Enter password: ")
        
        user = self.db_manager.find_user_by_email(email)
        if not user:
            print("User not found!")
            return False
        
        try:
            if user['algorithm'] == 'scrypt':
                is_valid = self.auth_manager.verify_scrypt(password, user['password'])
            else:  
                is_valid = self.auth_manager.verify_pbkdf2(password, user['password'])
            
            if is_valid:
                print("Login successful!")
                return True
            else:
                print("Invalid password!")
                return False
                
        except Exception as e:
            print(f"Error during login: {e}")
            return False
    
    def list_users(self):
        """List all users (for demonstration)"""
        users = self.db_manager.collection.find()
        print("\n--- Registered Users ---")
        for user in users:
            print(f"Email: {user['email']}, Algorithm: {user['algorithm']}")
    
    def run(self):
        while True:
            print("1. Register User")
            print("2. Login User")
            print("3. List Users")
            print("4. Exit")
            
            choice = input("Choose an option (1-4): ").strip()
            
            if choice == '1':
                self.register_user()
            elif choice == '2':
                self.login_user()
            elif choice == '3':
                self.list_users()
            elif choice == '4':
                self.db_manager.close_connection()
                print("Goodbye!")
                break
            else:
                print("Invalid choice!")

if __name__ == "__main__":
    try:
        app = AuthApp()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication interrupted!")
    except Exception as e:
        print(f"Application error: {e}")