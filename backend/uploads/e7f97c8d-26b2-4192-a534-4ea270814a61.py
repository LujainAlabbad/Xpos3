import os

# Vulnerability 1: Use of exec
exec("print('hello')")

# Vulnerability 2: Hardcoded password
password = "admin123"

# Vulnerability 3: SQL injection risk
query = "SELECT * FROM users WHERE name = '" + user_input + "'"

# Vulnerability 4: Using pickle
import pickle
data = pickle.loads(user_data)

