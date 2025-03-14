# Full Stack User CRUD Application

This project is a **full-stack user management application** built with Flask, MongoDB, and Vue.js. It parses user data from JSON and provides a complete RESTful API with CRUD operations.

---

## API Documentation

This Flask API interacts with a MongoDB database to perform CRUD operations.

### Endpoints

| Method   | Endpoint           | Description                  | Request Body Example     | Response              |
| -------- | ------------------ | ---------------------------- | ------------------------ | --------------------- |
| `GET`    | `/users/`          | Retrieve all users           | -                        | List of users         |
| `GET`    | `/users/<user_id>` | Retrieve a single user by ID | None                     | Single user object    |
| `POST`   | `/users/`          | Create a new user            | JSON (see example below) | Created user object   |
| `PUT`    | `/users/<user_id>` | Update an existing user      | JSON fields to update    | Updated user object   |
| `DELETE` | `/users/<user_id>` | Delete an existing user      | None                     | Deletion confirmation |

### JSON Example (for POST method)

```json
{
  "username": "example_user",
  "password": "securepass123",
  "roles": ["admin", "manager"],
  "preferences": { "timezone": "UTC" },
  "active": true
}
```

### JSON Example (for PUT method)

```json
{
  "username": "updateduser",
  "active": false
}
```

## Setup and Running the Project

### 1. Create and Activate the Virtual Environment

From your project's root directory (`full-stack-user-crud/`):

**Windows (PowerShell)/macOS/Linux:**

```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 2. Install Dependencies

```powershell
pip install -r server/requirements.txt
```

### 3. Ensure MongoDB is Running

Make sure MongoDB is running locally at:

```powershell
mongodb://localhost:27017/
```

### 4. Run the Flask Server

From your project's root directory, execute:

```powershell
python -m server.app
```

## Running Tests

To ensure that tests do not affect your main database, the tests use a separate test database.

### Step 1: Switch to Test Database

Manually update server/db.py before running tests:

```python
# server/db.py
db = get_database(testing=True)  # set True during testing
```

### Step 2: Run Pytest

From your project root directory, activate the environment and run:

```powershell
pytest server/tests/
```

This runs all available tests and provides a detailed report.
