# **SubsManager PostgreSQL Database**

## 🛠 **Tech Stack**

- **Database**: PostgreSQL
- **Containerization**: Docker
- **Schema Management**: SQL Scripts

## 📂 **Project Structure**

```
.                               # Project root directory
├── Dockerfile                  # Configuration file for building PostgreSQL Docker container
├── README.md                   # Document containing database description and information
├── run.sh                      # Shell script for running the database container
└── sqls                        # Directory containing SQL scripts
    ├── users.sql               # SQL script for creating and populating the users table
    └── subs.sql                # SQL script for creating and populating the subscriptions table
```  

## 🚀 **Installation and Execution**

### **Running PostgreSQL with Docker**
```bash
docker build -t subsmanager-db .
docker run -p 5432:5432 --name subsmanager-db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=asdf1234! -d subsmanager-db
```

## 🔑 **Database Configuration**
```env
POSTGRES_USER=postgres           # PostgreSQL username
POSTGRES_PASSWORD=asdf1234!      # PostgreSQL password
POSTGRES_DB=subs_service         # PostgreSQL database name
POSTGRES_PORT=5432               # PostgreSQL port (default: 5432)
```
