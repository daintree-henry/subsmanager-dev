# **SubsManager Subscription**

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
docker build -t subsmanager-subscription .
docker run -p 5000:5000 subsmanager-subscription
```

## 🔑 **Environment Variables**

```env
DB_USER='postgres'       # Database user name
DB_PASSWORD='asdf1234!'  # Database user password
DB_HOST='localhost'      # Database host
DB_PORT='5432'           # Database port
DB_NAME='subs_service'   # Database name
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

### **1. Create or Reactivate Subscription**
**Endpoint:** `POST /sub`

**Description:**
- Creates a new subscription for the user.
- If the user has a deactivated subscription for the same plan, it reactivates it.

**Request Headers:**
```http
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

**Request Body:**
```json
{
  "subscription_plan_id": 1,
  "start_date": "2024-03-01",
  "payment_method": "credit_card"
}
```

**Response:**
- **201 CREATED**: Subscription successfully created.
- **200 OK**: Subscription reactivated.
- **400 BAD REQUEST**: Missing required fields or invalid data.
- **409 CONFLICT**: An active subscription already exists.
- **500 INTERNAL SERVER ERROR**: If an error occurs during the process.

---

### **2. Get Subscription Details**
**Endpoint:** `GET /sub/<int:subscription_id>`

**Description:**
- Retrieves information about a specific subscription.

**Request Headers:**
```http
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
- **200 OK**: Returns subscription details.
- **403 FORBIDDEN**: User does not have permission to access this subscription.
- **404 NOT FOUND**: Subscription not found.
- **500 INTERNAL SERVER ERROR**: If an error occurs during the process.

---

### **3. Get Available Subscription Plans**
**Endpoint:** `GET /sub/plans`

**Description:**
- Retrieves a list of active subscription plans along with provider details.

**Request Headers:**
```http
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
- **200 OK**: Returns a list of available subscription plans.
- **500 INTERNAL SERVER ERROR**: If an error occurs during the process.

---

### **4. Get User's Subscription Plans**
**Endpoint:** `GET /sub/plans/user`

**Description:**
- Retrieves the subscription plans that the currently logged-in user has subscribed to.

**Request Headers:**
```http
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
- **200 OK**: Returns a list of the user's active subscriptions.
- **500 INTERNAL SERVER ERROR**: If an error occurs during the process.

---

### **5. Extend Subscription**
**Endpoint:** `POST /sub/<int:subscription_id>/extend`

**Description:**
- Extends an active subscription for the user.

**Request Headers:**
```http
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
- **200 OK**: Subscription successfully extended.
- **400 BAD REQUEST**: Cannot extend a canceled, expired, or suspended subscription.
- **403 FORBIDDEN**: Unauthorized access attempt.
- **404 NOT FOUND**: Subscription not found.
- **500 INTERNAL SERVER ERROR**: If an error occurs during the process.

---

### **6. Cancel Subscription**
**Endpoint:** `POST /sub/<int:subscription_id>/cancel`

**Description:**
- Cancels an active subscription for the user.

**Request Headers:**
```http
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
- **200 OK**: Subscription successfully canceled.
- **403 FORBIDDEN**: Unauthorized access attempt.
- **404 NOT FOUND**: Subscription not found.
- **500 INTERNAL SERVER ERROR**: If an error occurs during the process.

---

### **7. Create Subscription Payment**
**Endpoint:** `POST /sub/payments`

**Description:**
- Creates a new payment record for a user's subscription.

**Request Headers:**
```http
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

**Request Body:**
```json
{
  "user_subscription_id": 1,
  "amount_paid": 9.99,
  "payment_method": "credit_card"
}
```

**Response:**
- **201 CREATED**: Payment successfully recorded.
- **400 BAD REQUEST**: Missing required fields.
- **403 FORBIDDEN**: Unauthorized access attempt.
- **404 NOT FOUND**: Subscription not found.
- **500 INTERNAL SERVER ERROR**: If an error occurs during the process.

---

### **8. Get User's Subscription Payments**
**Endpoint:** `GET /sub/payments`

**Description:**
- Retrieves all subscription payments made by the currently logged-in user.

**Request Headers:**
```http
Authorization: Bearer <JWT_TOKEN>
```

**Query Parameters:**
- `page` (int, optional): Page number for pagination.
- `per_page` (int, optional): Number of items per page.
- `status` (string, optional): Filter payments by status.

**Response:**
- **200 OK**: Returns a paginated list of the user's subscription payments.
- **500 INTERNAL SERVER ERROR**: If an error occurs during the process.

---

This document provides an overview of the key API endpoints for managing subscriptions within the **SubsManager** system. If additional endpoints need to be documented, please let us know! 🚀

