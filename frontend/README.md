# **SubsManager Frontend**

## 🛠 **Tech Stack**

- **Frontend**: Vue.js, Tailwind CSS, Vite
- **API Request Management**: Axios
- **Containerization**: Docker

## 📂 **Project Structure**

```
.                               # Project root directory
├── Dockerfile                  # Configuration file for building Docker container
├── README.md                   # Document containing project description and information
├── create-project.sh           # Shell script for initial project setup
├── dev                         # Directory for development environment files
│   └── Dockerfile-local        # Docker configuration file for local development environment
├── index.html                  # Entry point HTML file for the application
├── nginx.conf                  # Nginx web server configuration file
├── package.json                # File defining project dependencies and scripts
├── postcss.config.js           # PostCSS configuration file (for CSS processing)
├── public                      # Directory for static files
│   ├── images                  # Directory for storing image files
│   └── vite.svg                # Vite framework logo image
├── run.sh                      # Shell script for running the application
├── src                         # Main directory for source code
│   ├── App.vue                 # Main Vue component
│   ├── api                     # Directory for API-related code
│   │   └── axios.js            # Axios HTTP client configuration file
│   ├── assets                  # Directory for project resources
│   │   ├── main.css            # Main CSS file
│   │   └── vue.svg             # Vue.js logo image
│   ├── components              # Directory for reusable Vue components
│   │   ├── Home.vue            # Home page component
│   │   ├── LoginForm.vue       # Login form component
│   │   ├── Payments.vue        # Payment-related component
│   │   ├── SubscriptionList.vue # Subscription list component
│   │   └── SubscriptionModal.vue # Subscription modal component
│   ├── config                  # Directory for configuration files
│   │   └── api.config.js       # API-related configuration file
│   ├── main.js                 # Entry point JavaScript file for Vue application
│   ├── router                  # Directory for Vue Router files
│   │   └── index.js            # Routing configuration file
│   └── store                   # Directory for Vuex state management files
│       ├── auth.js             # Authentication-related state management module
│       └── subscription.js     # Subscription-related state management module
├── tailwind.config.js          # Tailwind CSS framework configuration file
└── vite.config.js              # Vite build tool configuration file
```

## 🚀 **Installation and Execution**

### **Running Docker Container**
```bash
docker build -t subsmanager-frontend .
docker run -p 5173:5173 subsmanager-frontend
```

## 🔑 **Environment Variables**
```env
VITE_USER_API_URL=http://your-user-api-server:port              # User API server URL (default: http://localhost:5005)
VITE_SUBS_API_URL=http://your-subscription-api-server:port      # Subscription API server URL (default: http://localhost:5004)
VITE_RECO_API_URL=http://your-recommendation-api-server:port    # Recommendation API server URL (default: http://localhost:5003)
```
