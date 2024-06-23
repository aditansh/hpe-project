import sqlite3
import hashlib
import requests

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    conn = sqlite3.connect('security_system.db')
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        print("User registered successfully.")
    except sqlite3.IntegrityError:
        print("Username already exists.")
    conn.close()

def ban_user(username):
    conn = sqlite3.connect('security_system.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET is_banned = 1 WHERE username = ?', (username,))
    conn.commit()
    conn.close()
    print(f"User {username} has been banned.")

def login_user(username, password):
    conn = sqlite3.connect('security_system.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, password, is_banned FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    if user:
        user_id, hashed_password, is_banned = user
        if is_banned:
            print("This user is banned and cannot login.")
            return None
        if hashed_password == hash_password(password):
            print("Login successful.")
            return user_id
        else:
            print("Incorrect password.")
            return None
    else:
        print("User not found.")
        return None

def check_python_vulnerability(python_version):
    url = f"https://api.example.com/vulnerabilities?version={python_version}"  # Hypothetical API URL
    try:
        response = requests.get(url)
        response.raise_for_status()
        vulnerabilities = response.json()
        if vulnerabilities:
            print(f"Vulnerabilities found in Python {python_version}:")
            for vulnerability in vulnerabilities:
                print(f"- {vulnerability['title']}: {vulnerability['description']}")
                print(f"  Fix Version: {vulnerability['fix_version']}")
        else:
            print(f"No known vulnerabilities found for Python {python_version}.")
    except requests.exceptions.RequestException as e:
        print(f"Error checking vulnerabilities: {e}")

while True:
    choice = input("Enter 'register', 'login', 'ban', 'check', or 'exit': ").strip().lower()
    if choice == 'register':
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()
        register_user(username, password)
    elif choice == 'login':
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()
        user_id = login_user(username, password)
    elif choice == 'ban':
        username = input("Enter the username to ban: ").strip()
        ban_user(username)
    elif choice == 'check':
        python_version = input("Enter the Python version to check (e.g., 3.9.1): ").strip()
        check_python_vulnerability(python_version)
    elif choice == 'exit':
        break
    else:
        print("Invalid choice. Please try again.")