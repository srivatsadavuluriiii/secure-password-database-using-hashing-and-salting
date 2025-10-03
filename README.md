# Secure Password Database (Hashing and Salting)

Project that demonstrates securely storing user passwords using modern hashing and salting techniques. The repository contains a small Python application which manages password storage and verification while avoiding plaintext storage of credentials.

## Features

- Demonstrates hashing and salting of passwords for secure storage
- Minimal CLI/API structure suitable for extension or learning
- Clear examples of responsible secret handling and storage patterns

## Requirements

- Python 3.10+ (3.11 recommended)
- Virtual environment (recommended)
- Dependencies listed in `requirements.txt`

## Installation

1. Clone the repository (if you haven't already):

   git clone https://github.com/srivatsadavuluriiii/secure-password-database-using-hashing-and-salting.git
   cd secure-password-database-using-hashing-and-salting

2. Create and activate a virtual environment:

   python -m venv .venv
   source .venv/bin/activate

3. Install dependencies:

   pip install -r requirements.txt

## Project structure

- `app.py` - Application entry point / example usage
- `auth_manager.py` - Password hashing and verification logic
- `database.py` - Simple storage abstraction (file or in-memory)
- `config.py` - Configuration constants and settings
- `requirements.txt` - Python dependencies

## Usage

Run the main application to see example flows or to manually exercise functions:

   python app.py

Refer to `auth_manager.py` for functions to create hashed passwords and verify them. If you plan to import the modules, the expected behavior is:

- `hash_password(plain_password)` -> returns a salted, securely hashed password string
- `verify_password(plain_password, stored_hash)` -> returns True if match, False otherwise

## Configuration

Keep secrets and environment-specific settings out of source control. Use environment variables or a local `config` file that is excluded by `.gitignore`.

## Security considerations

- Always use a vetted password hashing function (bcrypt, Argon2, PBKDF2 with adequate iterations). This project is intended for learning; for production, use a maintained library such as `bcrypt` or `argon2-cffi`.
- Do not log plaintext passwords. Avoid storing secrets in source control.
- Rotate salts and hashing parameters as best practice when threat models change.

## Testing

Add unit tests for the hashing and verification logic. Example tests should verify:

- Hashing produces different hashes for the same password when salts differ
- Verification returns True for correct password and False otherwise

## Contribution

Contributions are welcome. Open an issue to discuss major changes. Keep changes focused and include tests for new behavior.

