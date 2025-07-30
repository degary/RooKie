# 安装部署

## 📋 概述

本文档指导您完成 Rookie 项目的环境搭建和安装部署。

## 🔧 系统要求

### 基础环境
- **Python**: 3.8+ (推荐 3.11+)
- **数据库**: SQLite (默认) / PostgreSQL / MySQL
- **操作系统**: Windows / macOS / Linux

### 推荐配置
- **内存**: 2GB+
- **存储**: 1GB+ 可用空间
- **网络**: 稳定的互联网连接

## 📦 安装步骤

### 1. 克隆项目

```bash
git clone https://github.com/degary/RooKie.git
cd RooKie
```

### 2. 创建虚拟环境

```bash
# 使用 venv
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 数据库配置

#### 使用SQLite (默认)
```bash
# 无需额外配置，直接进行数据库迁移
python manage.py migrate
```

#### 使用PostgreSQL
```bash
# 1. 安装PostgreSQL驱动
pip install psycopg2-binary

# 2. 修改配置文件
# 编辑 Rookie/settings/dev.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'rookie_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# 3. 创建数据库
createdb rookie_db

# 4. 运行迁移
python manage.py migrate
```

### 5. 创建超级用户

```bash
# 方法1: 交互式创建
python manage.py createsuperuser

# 方法2: 使用演示数据
python examples/admin_demo.py
```

### 6. 初始化系统数据

```bash
# 初始化权限系统
python examples/setup_permissions.py

# 配置第三方登录 (可选)
python examples/setup_third_party_auth.py
```

## ✅ 验证安装

### 1. 启动开发服务器

```bash
python manage.py runserver
```

### 2. 访问应用

- **前台首页**: http://127.0.0.1:8000
- **登录页面**: http://127.0.0.1:8000/login/
- **管理后台**: http://127.0.0.1:8000/admin/

### 3. 测试API

```bash
# 测试API接口
curl http://127.0.0.1:8000/api/users/third_party_providers/
```

## 🔧 环境配置

### 开发环境
```bash
# 设置环境变量
export DJANGO_ENV=dev
python manage.py runserver
```

### 测试环境
```bash
export DJANGO_ENV=acc
python manage.py runserver
```

### 生产环境
```bash
export DJANGO_ENV=prod
export SECRET_KEY="your-secret-key"
python manage.py collectstatic --noinput
python manage.py migrate
gunicorn Rookie.wsgi:application --bind 0.0.0.0:8000
```

## 🐳 Docker 部署

### 1. 构建镜像

```bash
# 创建 Dockerfile
cat > Dockerfile << EOF
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
EOF

# 构建镜像
docker build -t rookie .
```

### 2. 运行容器

```bash
# 开发环境
docker run -p 8000:8000 -e DJANGO_ENV=dev rookie

# 生产环境
docker run -p 8000:8000 -e DJANGO_ENV=prod -e SECRET_KEY="your-key" rookie
```

## ❗ 常见问题

### Q: pip install 失败
```bash
# 升级pip
pip install --upgrade pip

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

### Q: 数据库连接失败
```bash
# 检查数据库服务状态
# 确认配置文件中的数据库参数
# 检查防火墙设置
```

### Q: 端口被占用
```bash
# 查看端口占用
lsof -i :8000

# 使用其他端口
python manage.py runserver 8001
```

## 🔗 下一步

安装完成后，继续阅读：
- [快速开始](quick-start.md) - 项目启动和基本使用
- [第一个API](first-api.md) - API调用示例
