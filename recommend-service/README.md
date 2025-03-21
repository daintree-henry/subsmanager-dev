# **SubsManager Recommend**

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
```

## 🚀 **Installation and Execution**

### **Running the Application with Docker**

```bash
docker build -t subsmanager-recommend .
docker run -p 5000:5000 subsmanager-recommend
```

## 🔑 **Environment Variables**

```env
SUB_URL='http://localhost:5004'       # URI of the subscription module
RECOMMEND_COUNT='1'                   # Number of subscriptions to recommend
JWT_SECRET_KEY='mJMLk2qwEFKp1Lx2FatzwVOA6-3FjMqkLEAWu74uCU9'    # Secret key for JWT tokens
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
**Endpoint:** `POST /recommend`

**Description:**
- Recommends subscription plans that the current user has not subscribed to.
- Filters out plans from providers that the user is already subscribed to.
- Selects one random plan from each provider.
- Returns up to the number of recommendations specified in `RECOMMEND_COUNT`.

**Request Headers:**
```http
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
- **200 OK**: Returns a list of recommended subscription plans.
- **500 INTERNAL SERVER ERROR**: If an error occurs during the recommendation process.

**Example Response:**
```json
{
  "recommends": [
    {
      "id": 123,
      "name": "Premium Plan",
      "provider_name": "Netflix"
    },
    {
      "id": 456,
      "name": "Music Unlimited",
      "provider_name": "Spotify"
    }
  ]
}
```


