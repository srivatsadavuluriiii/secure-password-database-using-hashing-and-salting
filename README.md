# Secure Password Database (Hashing and Salting)

This repository demonstrates secure password storage using strong hashing and salting algorithms. It contains a small Python application that provides user registration and authentication flows, backed by MongoDB for storage. The project is intended for learning and small prototypes — review the Security considerations below before using any part of this code in production.

## Quick start — what to run

1. Clone the repository and change into the project directory:

    git clone https://github.com/srivatsadavuluriiii/secure-password-database-using-hashing-and-salting.git
    cd secure-password-database-using-hashing-and-salting

2. Create and activate a virtual environment:

    python -m venv .venv
    source .venv/bin/activate

3. Install dependencies:

    pip install -r requirements.txt

4. Ensure MongoDB is running and accessible (default URI: `mongodb://localhost:27017/`). To override, set `MONGO_URI` in your environment or a `.env` file.

5. Run the application:

    python app.py

The interactive menu lets you register users, log in, and list registered users.

## File-by-file overview (detailed)

- `app.py`
   - Entry point for the interactive demo application.
   - Implements `AuthApp` which wires together `DatabaseManager` and `AuthManager`.
   - Menu options:
      - Register User: prompts for email and password (hidden input), chooses hashing algorithm (`scrypt` or `pbkdf2`), and stores the user record.
      - Login User: prompts for email and password, looks up the user in the database, and calls the correct verification routine based on the stored `algorithm` field.
      - List Users: prints stored users (email and algorithm) — included for demonstration only and not safe for production use.

- `auth_manager.py`
   - Implements `AuthManager` and the hashing/verification functionality using `passlib` wrappers.
   - Public methods and behavior:
      - `hash_with_scrypt(password)`: produces a scrypt-based hash using parameters from `config.Config`.
      - `hash_with_pbkdf2(password)`: produces a PBKDF2-HMAC-SHA256 hash using configured rounds.
      - `verify_scrypt(password, hashed)`: verifies a plaintext password against a scrypt hash.
      - `verify_pbkdf2(password, hashed)`: verifies a plaintext password against a PBKDF2 hash.
      - `create_user_data(email, password, algorithm)`: convenience method that hashes the provided password with the chosen algorithm and returns a dict with `email`, `password` (the hash string), `algorithm`, and `created_at` timestamp.
   - Notes:
      - `passlib` produces complete encoded hash strings which include salt and parameters; storing the full encoded string is recommended (and how this project stores passwords).
      - The code uses `passlib.hash.scrypt` and `passlib.hash.pbkdf2_sha256`.

- `database.py`
   - Implements `DatabaseManager`, a thin wrapper around `pymongo.MongoClient`.
   - Behavior:
      - Connects to MongoDB using `Config.MONGO_URI` and selects the configured database and collection.
      - Ensures a unique index on the `email` field.
      - `insert_user(user_data)`: inserts a user document and returns True on success, False on failure or duplicate email.
      - `find_user_by_email(email)`: fetches a single user document by email.
      - `close_connection()`: closes the MongoDB connection.
   - Notes:
      - For learning, the project stores the entire passlib hash string in the `password` field and records the algorithm used in `algorithm`.
      - Replace this storage abstraction with a real database access pattern if using in production (e.g., parameterized queries, ORM, connection pooling, secrets management).

- `config.py`
   - Loads environment variables through `python-dotenv` and exposes a `Config` class with constants:
      - `MONGO_URI`: default `mongodb://localhost:27017/`.
      - `DATABASE_NAME`, `COLLECTION_NAME`: default database/collection for user documents.
      - `SCRYPT_N`, `SCRYPT_R`, `SCRYPT_P`: scrypt cost parameters used by `passlib` wrapper.
      - `PBKDF2_ROUNDS`: iteration count for PBKDF2.
   - To override configuration, set environment variables (for `MONGO_URI`) or modify the file locally (not recommended for secrets).

## What each file does — quick call reference

- `auth_manager.hash_with_scrypt(password)` -> returns encoded scrypt hash string
- `auth_manager.hash_with_pbkdf2(password)` -> returns encoded PBKDF2-SHA256 hash string
- `auth_manager.verify_scrypt(password, stored_hash)` -> True/False
- `auth_manager.verify_pbkdf2(password, stored_hash)` -> True/False
- `database.DatabaseManager.insert_user(user_data)` -> True on success, False on error/duplicate
- `database.DatabaseManager.find_user_by_email(email)` -> dict or None

## Security considerations (expanded)

- Use production-ready libraries and parameters:
   - For production choose Argon2 or bcrypt/modern scrypt parameters appropriate for your hardware.
   - The `passlib` wrappers used here are convenient for examples; verify algorithm parameters before deploying.

- Secrets and environment handling:
   - Do not commit `MONGO_URI` with credentials to source control. Use environment variables or a secrets manager.
   - Do not add a `.env` file to source control; add it to `.gitignore`.

- Logging and data exposure:
   - Remove demonstration helpers (e.g., `list_users`) before production. Avoid printing user lists or hashes.

## Testing recommendations

- Add unit tests (pytest recommended) for `AuthManager` functions: ensure expected behavior for hashing and verification across algorithms and incorrect inputs.
- Example test cases:
   - Same password hashed twice yields different encoded results (due to different salts).
   - Correct password verifies True; wrong password verifies False.
   - `create_user_data` returns a dict with expected keys and non-empty `password`.

## Contribution and maintenance notes

- File issues for design changes. Keep cryptographic parameter changes in a single place (`config.py`) and document migration steps when changing parameters that affect verify behavior.
- Add a `LICENSE` file if you intend to open-source the project.


