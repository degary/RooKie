# Rookie

<div align="center">

![Rookie Logo](https://gw.alipayobjects.com/zos/rmsportal/KDpgvguMpGfqaHPjicRK.svg)

**An out-of-the-box Django enterprise web application framework**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2+-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

English | [简体中文](README.md)

</div>

## 📖 Project Overview

Rookie is a Django web application framework designed for enterprise-level applications, providing complete user management, permission control, third-party login integration, and other features. Through modular design and rich toolsets, it helps developers quickly build secure and scalable enterprise applications.

### 🎯 Design Philosophy

- **Out-of-the-box**: Provides complete enterprise-level functional modules
- **Security First**: Built-in multi-layer security protection mechanisms
- **Easy to Extend**: Plugin architecture supporting custom extensions
- **Developer Friendly**: Rich toolsets and detailed documentation

## ✨ Core Features

### 🔐 Complete Authentication System
- **Multiple Authentication Methods**: Token, Session, Third-party OAuth
- **Security Policies**: Password policies, login restrictions, session management
- **User Lifecycle**: Registration, verification, activation, deactivation

### 🔑 Fine-grained Permission Control
- **Module-level Permissions**: Permission division based on business modules
- **Role Management**: Support for user groups and direct authorization
- **Permission Inheritance**: Department-level permission inheritance mechanism
- **Dynamic Permissions**: Runtime permission checking and management

### 🌐 Third-party Login Integration
- **Enterprise Platforms**: DingTalk, WeChat Work, Feishu
- **QR Code Login**: QR code login support
- **User Synchronization**: Automatic synchronization of organizational structure and user information
- **Plugin Architecture**: Easy to extend new login methods

### 📊 Unified API Response
- **Standard Format**: Unified success/error response structure
- **Error Handling**: Global exception handling and error code management
- **API Documentation**: Auto-generated Swagger/OpenAPI documentation
- **Version Control**: API version management support

### 🎨 Modern Management Interface
- **Ant Design**: Beautiful interface based on Ant Design
- **Responsive Design**: Support for desktop and mobile
- **Theme Customization**: Support for dark/light theme switching
- **Internationalization**: Multi-language support

### 🛠️ Development Toolset
- **Logging System**: High-performance logging based on Loguru
- **Utility Modules**: Rich utility functions and decorators
- **Testing Support**: Complete testing framework and examples
- **Deployment Solutions**: Docker containerized deployment

## 🚀 Quick Start

### Requirements

- Python 3.8+
- Django 4.2+
- PostgreSQL 12+ (recommended for production)

### Installation

```bash
# 1. Clone the project
git clone https://github.com/degary/RooKie.git
cd RooKie

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Environment configuration
cp .env.example .env
# Edit .env file to configure database and other settings

# 5. Initialize database
python manage.py migrate

# 6. Create demo data
python examples/admin_demo.py

# 7. Start development server
python manage.py runserver
```

### Access Application

- **Admin Panel**: http://127.0.0.1:8000/admin/
- **API Documentation**: http://127.0.0.1:8000/api/docs/
- **Login Page**: http://127.0.0.1:8000/login/

**Default Admin Account**: 
- Email: `admin@example.com`
- Password: `password123`

## 📡 API Usage Examples

### User Authentication

```bash
# User login
curl -X POST http://127.0.0.1:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "password123"
  }'

# Response example
{
  "success": true,
  "code": 200,
  "message": "Login successful",
  "data": {
    "user": {
      "id": "uuid-here",
      "email": "admin@example.com",
      "username": "admin"
    },
    "token": "your-token-here"
  },
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### Token Authentication

```bash
# Access protected API with Token
curl -H "Authorization: Token your-token-here" \
     http://127.0.0.1:8000/api/users/profile/

# Get user module permissions
curl -H "Authorization: Token your-token-here" \
     http://127.0.0.1:8000/api/users/my_modules/
```

### Third-party Login

```bash
# Get available third-party login providers
curl http://127.0.0.1:8000/api/users/third_party_providers/

# Response example
{
  "success": true,
  "data": {
    "providers": [
      {
        "name": "dingtalk",
        "display_name": "DingTalk Login",
        "corp_id": "your-corp-id",
        "client_id": "your-client-id"
      }
    ]
  }
}
```

## 🏗️ Technical Architecture

### Backend Technology Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| Django | 4.2+ | Web Framework |
| Django REST Framework | 3.14+ | API Framework |
| PostgreSQL | 12+ | Database |
| Redis | 6+ | Cache |
| Loguru | 0.7+ | Logging System |
| Gunicorn | 21+ | WSGI Server |

### Project Structure

```
RooKie/
├── Rookie/                 # Django project configuration
│   ├── settings/          # Environment-specific settings
│   │   ├── base.py       # Base configuration
│   │   ├── dev.py        # Development environment
│   │   └── prod.py       # Production environment
│   ├── urls.py           # URL configuration
│   └── wsgi.py           # WSGI entry point
├── users/                 # User management module
│   ├── models.py         # User models
│   ├── views.py          # API views
│   ├── serializers.py    # Serializers
│   └── admin.py          # Admin interface
├── plugins/               # Third-party login plugins
│   ├── base.py           # Plugin base class
│   ├── dingtalk/         # DingTalk login
│   └── wechat_work.py    # WeChat Work
├── utils/                 # Utility modules
│   ├── response/         # Response wrapper
│   ├── auth/             # Permission utilities
│   ├── logger.py         # Logging utilities
│   └── README.md         # Utility documentation
├── templates/             # Template files
├── static/                # Static files
├── docs/                  # Project documentation
├── examples/              # Example code
├── tests/                 # Test code
├── docker-compose.yml     # Docker orchestration
├── Dockerfile            # Docker image
├── requirements.txt      # Python dependencies
└── manage.py             # Django management script
```

## 📚 Documentation

### 📖 User Guide
- [📦 Installation](docs/getting-started/installation.md) - Detailed installation and configuration guide
- [⚡ Quick Start](docs/getting-started/quick-start.md) - 5-minute quick experience
- [🔐 Authentication](docs/user-guide/authentication.md) - Login authentication and Token usage
- [🔑 Permission Management](docs/user-guide/permissions.md) - Permission configuration and management
- [📊 Admin Panel](docs/user-guide/admin-panel.md) - Admin panel usage guide

### 🛠️ Developer Guide
- [🏗️ System Architecture](docs/developer-guide/architecture.md) - Project architecture and design philosophy
- [📝 Coding Standards](docs/developer-guide/coding-standards.md) - Code standards and best practices
- [🧪 Testing Guide](docs/developer-guide/testing.md) - Testing methods and specifications
- [🚀 Deployment Guide](docs/developer-guide/deployment.md) - Production environment deployment

### 📡 API Reference
- [🔐 Authentication API](docs/api-reference/authentication.md) - Login, registration, Token management
- [👥 User API](docs/api-reference/users.md) - User management related interfaces
- [🔑 Permission API](docs/api-reference/permissions.md) - Permission query and management
- [📋 Response Format](docs/api-reference/responses.md) - Unified response format description

### 🎓 Tutorials
- [🔑 Token Authentication Tutorial](docs/tutorials/token-auth-tutorial.md) - Complete Token authentication practice
- [🔐 Permission Configuration Tutorial](docs/tutorials/permission-tutorial.md) - Permission system configuration practice
- [🌐 Third-party Login Tutorial](docs/tutorials/third-party-login.md) - Third-party login integration

## 🐳 Docker Deployment

### Development Environment

```bash
# Start development environment
docker-compose up -d

# View logs
docker-compose logs -f web

# Enter container
docker-compose exec web bash
```

### Production Environment

```bash
# Set environment variables
export SECRET_KEY="your-secret-key"
export DB_PASSWORD="your-db-password"

# Start production environment
docker-compose -f docker-compose.yml up -d

# Initialize database
docker-compose exec web python manage.py migrate
docker-compose exec web python examples/admin_demo.py
```

## 🔧 Configuration

### Environment Variables

```bash
# .env file example
DJANGO_ENV=dev                    # Environment: dev/prod
SECRET_KEY=your-secret-key        # Django secret key
DEBUG=True                        # Debug mode

# Database configuration
DB_HOST=localhost
DB_NAME=rookie
DB_USER=rookie
DB_PASSWORD=password

# Third-party login configuration
DINGTALK_CORP_ID=your-corp-id
DINGTALK_CLIENT_ID=your-client-id
DINGTALK_CLIENT_SECRET=your-secret
```

### Third-party Login Configuration

Add in the admin panel's "Third-party Authentication Configuration":

```json
{
  "corp_id": "your-dingtalk-corp-id",
  "client_id": "your-client-id",
  "client_secret": "your-client-secret",
  "redirect_uri": "http://your-domain.com/api/users/third_party_callback/"
}
```

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run specific module tests
python manage.py test users

# Generate coverage report
coverage run --source='.' manage.py test
coverage report
coverage html
```

## 🤝 Contributing

We welcome all forms of contributions! Please check the [Contributing Guide](CONTRIBUTING.md) for detailed information.

### Contribution Process

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Create a Pull Request

### Development Standards

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) code standards
- Use [Conventional Commits](https://www.conventionalcommits.org/) commit standards
- Write unit tests and documentation
- Ensure code coverage > 80%

## 📈 Roadmap

### v1.1.0 (Planned)
- [ ] Mobile adaptation optimization
- [ ] More third-party login support (GitHub, Google)
- [ ] Visual permission system management
- [ ] Operation audit logs

### v1.2.0 (Planned)
- [ ] Microservice architecture support
- [ ] GraphQL API
- [ ] Real-time notification system
- [ ] Data analysis dashboard

View complete roadmap: [TODO.md](TODO.md)

## 🆘 Troubleshooting

### Common Issues

**Q: Database connection error on startup?**
A: Check database configuration and connection information, ensure database service is running.

**Q: Third-party login not working after configuration?**
A: Check callback URL configuration, ensure domain and port are correct.

**Q: Token authentication failed?**
A: Confirm Token format is correct, should be `Token your-token-here`.

More solutions: [Troubleshooting Guide](docs/troubleshooting/common-issues.md)

## 📞 Get Help

- 📧 **Email Support**: support@rookie.com
- 💬 **Community Discussion**: [GitHub Discussions](https://github.com/degary/RooKie/discussions)
- 🐛 **Issue Reports**: [GitHub Issues](https://github.com/degary/RooKie/issues)
- 📖 **Online Documentation**: [Project Documentation](https://rookie-docs.com)

## 🙏 Acknowledgments

Thanks to all developers and users who contributed to the Rookie project!

Special thanks to the following open source projects:
- [Django](https://www.djangoproject.com/) - Web Framework
- [Django REST Framework](https://www.django-rest-framework.org/) - API Framework
- [SimpleUI](https://github.com/newpanjing/simpleui) - Admin Interface
- [Loguru](https://github.com/Delgan/loguru) - Logging System

## 📄 License

This project is open sourced under the [MIT License](LICENSE).

---

<div align="center">

**If this project helps you, please give us a ⭐️**

Made with ❤️ by [degary](https://github.com/degary)

</div>