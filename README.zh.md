🌐 Select your language:  
[English](README.en.md) | [한국어](README.ko.md) | [日本語](README.jp.md)

### **订阅管理器 (SubsManager)**

订阅管理器 (SubsManager) 是一个基于微服务架构的 Web 应用程序，旨在作为一个实践或教育工具，帮助用户在一个集中的平台上管理他们的订阅服务。

## 🏗️ **系统架构**

SubsManager 采用微服务架构，由五个独立的模块组成：

1. [**前端模块**](./frontend/README.md): 使用现代 Web 技术构建的用户界面，通过 REST API 与后端服务通信  
2. [**PostgreSQL 数据库**](./postgresql/README.md): 存储所有持久化的应用数据  
3. [**推荐服务**](./recommend-service/README.md): 分析用户偏好，推荐新的订阅服务（目前为演示目的进行模拟推荐）  
4. [**订阅管理服务**](./subscription-service/README.md): 处理核心的订阅管理功能  
5. [**用户服务**](./user-service/README.md): 管理用户身份验证、授权和用户资料  
    
## 📌 **核心功能**

- **订阅服务管理**：添加、修改、删除订阅  
- **到期通知**：在订阅到期前向用户发送通知  
- **支付历史管理**：查看用户的支付历史记录  
- **推荐系统**：根据用户兴趣推荐新的订阅服务  

## 📄 **许可证**
本项目遵循 MIT 许可证。更多详情请参阅 [LICENSE](LICENSE.md) 文件。

## 📧 **联系方式**
如果您对本项目有任何疑问或希望贡献代码，请通过以下电子邮件联系我们。

📩 **daintree.henry@gmail.com**