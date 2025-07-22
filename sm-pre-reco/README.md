# **SubsManager Pre Recomandation**

## 🛠 **Tech Stack**
This module pre-generates daily subscription recommendations for all users and stores them in Redis.  
It is designed to run as a batch job during off-peak hours to reduce latency for the main user-facing service.

---

## 🛠 Tech Stack

- **Language**: Python 3.9+
- **Dependencies**: `requests`, `redis`
- **Containerization**: Docker

---

## 📂 Project Structure

```

sm-pre-reco/
├── config.py               # Configuration file for environment variables
├── run.py                  # Main batch script
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker image definition
└── .env                    # Environment variables file

````

---

## 🚀 Running the Job

### Build Docker image

```bash
docker build -t sm-pre-reco .
````

### Run with environment variables

```bash
docker run --env-file .env sm-pre-reco
```

---

## 🔑 Environment Variables

```env
SUB_URL=http://sm-subs                  # Subscription module URL
USER_URL=http://sm-user                 # User module URL

REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=redispassword

RECOMMEND_COUNT=2                       # Number of recommendations per user
RECOMMEND_CACHE_TTL_SECOND=86400       # Cache TTL in seconds (default: 24 hours)
```

---

## ⚙️ How It Works

1. Fetch the full list of users from `sm-user`
2. For each user:

   * Fetch their subscribed plans
   * Recommend new plans (1 per provider, excluding already subscribed ones)
3. Cache the result to Redis with a key: `user:{user_id}:recommendation`

---

## 🧪 Example Log Output

```
[INFO] Starting recommendation cache generation
[OK] user:1001 recommendation cached
[OK] user:1002 recommendation cached
[SKIP] user:1003 has no available recommendations
[DONE] Job completed
```

---

## 📌 Notes

* The `/users/internal` endpoint used in `sm-user` should **not require authentication**, but must be protected from external access.
* Use network policies or ingress whitelisting to ensure this route is only accessible internally.
* This module does **not expose any API endpoint** — it runs once and exits.
