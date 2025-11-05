from flask import Flask, request, jsonify
from flask_cors import CORS
from database import DatabaseManager
from auth_manager import AuthManager
from datetime import datetime
import os

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://localhost:3001"], supports_credentials=True)

# Initialize managers (verbose=False to reduce console output in API)
db_manager = DatabaseManager(verbose=False)
auth_manager = AuthManager()

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "message": "API is running"}), 200

@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        confirm_password = data.get('confirmPassword', '')
        algorithm = data.get('algorithm', 'scrypt').strip().lower()
        
        # Validation
        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400
        
        if password != confirm_password:
            return jsonify({"error": "Passwords do not match"}), 400
        
        if len(password) < 8:
            return jsonify({"error": "Password must be at least 8 characters long"}), 400
        
        if algorithm not in ['scrypt', 'pbkdf2']:
            algorithm = 'scrypt'
        
        # Create user data
        user_data = auth_manager.create_user_data(email, password, algorithm)
        
        # Insert into database
        success = db_manager.insert_user(user_data, verbose=False)
        if success:
            return jsonify({
                "message": "User registered successfully",
                "email": email
            }), 201
        else:
            return jsonify({"error": "User with this email already exists"}), 409
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400
        
        # Find user
        user = db_manager.find_user_by_email(email)
        if not user:
            return jsonify({"error": "Invalid email or password"}), 401
        
        # Verify password
        try:
            if user['algorithm'] == 'scrypt':
                is_valid = auth_manager.verify_scrypt(password, user['password'])
            else:
                is_valid = auth_manager.verify_pbkdf2(password, user['password'])
            
            if is_valid:
                return jsonify({
                    "message": "Login successful",
                    "email": user['email'],
                    "algorithm": user['algorithm']
                }), 200
            else:
                return jsonify({"error": "Invalid email or password"}), 401
                
        except Exception as e:
            return jsonify({"error": "Authentication failed"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/verify', methods=['POST'])
def verify():
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        
        if not email:
            return jsonify({"error": "Email is required"}), 400
        
        user = db_manager.find_user_by_email(email)
        if user:
            return jsonify({"exists": True}), 200
        else:
            return jsonify({"exists": False}), 200
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    import socket
    
    # Try to find an available port starting from 5000
    port = int(os.environ.get('PORT', 5000))
    max_attempts = 10
    
    for attempt in range(max_attempts):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        
        if result != 0:
            # Port is available
            break
        else:
            # Port is in use, try next port
            port += 1
    
    print(f"Starting Flask API server on http://0.0.0.0:{port}")
    print(f"API endpoints available at http://localhost:{port}/api")
    app.run(debug=True, host='0.0.0.0', port=port)

