🌐 Select your language:  
[한국어](README.ko.md) | [日本語](README.jp.md) | [中文](README.zh.md)

# **SubsManager**

The SubsManager is a microservices-based web application designed as a practice or educational tool to help users manage their subscription services in one centralized platform.

## 🏗️ **System Architecture**

SubsManager is built using a microservices architecture, consisting of five distinct modules:
SubsManager consists of five distinct microservices:

1. [**Front-End Module**](./frontend/README.md): The user interface built with modern web technologies that communicates with backend services via REST APIs
2. [**PostgreSQL Database**](./postgresql/README.md): Stores all persistent application data
3. [**Recommendation Service**](./recommend-service/README.md): Analyzes user preferences to suggest new subscription services (currently simulates recommendations for demonstration purposes)
4. [**Subscription Service**](./subscription-service/README.md): Handles core subscription management functionality 
5. [**User Service**](./user-service/README.md): Manages authentication, authorization, and user profiles

## 📌 **Key Features**

- **Subscription Service Management**: Add, modify, delete subscriptions
- **Expiration Notifications**: Provide notifications to users before subscriptions expire
- **Payment History Management**: View user's payment history
- **Recommendation System**: Recommend new subscription services based on user interests

## 📄 **License**
This project is licensed under the MIT License. For more details, please refer to the [LICENSE](LICENSE.md) file.

## 📧 **Contact**
If you have questions about this project or wish to contribute, please contact us at the email below.

📩 **daintree.henry@gmail.com**