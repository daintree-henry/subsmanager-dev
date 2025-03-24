# **SubsManager User**

## 🛠 **Tech Stack**

- **Backend**: Flask, Flask-SQLAlchemy, Flask-JWT-Extended
- **Database**: PostgreSQL
- **Containerization**: Docker

## 📂 **Project Structure**

```
.                                 # Project root directory
├── API-TEST.http                 # API testing script
├── Dockerfile                    # Configuration file for building Docker container
├── requirements.txt              # Python dependencies
├── run.py                        # Entry point script to run the application
└── app                           # Application source code
    ├── __init__.py               # Package initializer
    ├── config.py                 # Configuration file for application settings
    └── routes.py                 # API route definitions
    └── models.py                 # Data models and database schema definitions
```

## 🚀 **Installation and Execution**

### **Running the Application with Docker**

```bash
docker build -t subsmanager-user .
docker run -p 5000:5000 subsmanager-user
```

## 🔑 **Environment Variables**

```env
DB_USER='postgres'       # Database user name
DB_PASSWORD='asdf1234!'  # Database user password
DB_HOST='localhost'      # Database host
DB_PORT='5432'           # Database port
DB_NAME='user_service'   # Database name
JWT_SECRET_KEY='mJMLk2qwEFKp1Lx2FatzwVOA6-3FjMqkLEAWu74uCU9' # Secret key for JWT tokens
```

## 📦 **Dependencies**

- Flask
- Flask-SQLAlchemy
- Flask-JWT-Extended
- psycopg2-binary
- Werkzeug
- Flask-Caching
- python-dateutil
- flask-cors

## 📌 **API Endpoints**

### **1. User Registration**
**Endpoint:** `POST /users/register`

**Description:**
- Registers a new user.
- Checks if the email or username is already in use.

**Request Headers:**
```http
Content-Type: application/json
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "user123",
  "full_name": "John Doe",
  "password": "securepassword"
}
```

**Response:**
- **201 CREATED**: User successfully registered.
- **400 BAD REQUEST**: Email or username already exists.
- **500 INTERNAL SERVER ERROR**: If an error occurs during the process.

**Example Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "user123",
  "full_name": "John Doe"
}
```

---

### **2. User Login**
**Endpoint:** `POST /users/login`

**Description:**
- Authenticates a user and returns a JWT access token.

**Request Headers:**
```http
Content-Type: application/json
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:**
- **200 OK**: Login successful, returns JWT token.
- **400 BAD REQUEST**: Missing email or password.
- **401 UNAUTHORIZED**: Invalid credentials.
- **500 INTERNAL SERVER ERROR**: If an error occurs during the process.

**Example Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsIn...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "user123",
    "full_name": "John Doe"
  },
  "token_type": "bearer"
}
```

---

### **3. Get Current User Info**
**Endpoint:** `GET /users/me`

**Description:**
- Retrieves the currently logged-in user's information.

**Request Headers:**
```http
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
- **200 OK**: Returns user details.
- **401 UNAUTHORIZED**: Token is missing, expired, or invalid.
- **404 NOT FOUND**: User not found.
- **500 INTERNAL SERVER ERROR**: If an error occurs during the process.

**Example Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "user123",
  "full_name": "John Doe"
}
```

---

This document provides an overview of the key authentication endpoints for **SubsManager**. If additional endpoints need to be documented, please let us know! 🚀

