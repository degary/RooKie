# Rookie 安装部署指南

## 📋 系统要求

### 最低要求
- **操作系统**: Linux/macOS/Windows
- **Python**: 3.8+
- **内存**: 2GB RAM
- **磁盘**: 5GB 可用空间
- **网络**: 互联网连接（用于第三方登录）

### 推荐配置
- **操作系统**: Ubuntu 20.04 LTS / CentOS 8
- **Python**: 3.11+
- **内存**: 4GB+ RAM
- **磁盘**: 20GB+ SSD
- **数据库**: PostgreSQL 14+
- **缓存**: Redis 6+

## 🚀 快速安装

### 1. 获取源码

```bash
# 方式一：Git克隆（推荐）
git clone https://github.com/degary/RooKie.git
cd RooKie

# 方式二：下载压缩包
wget https://github.com/degary/RooKie/archive/main.zip
unzip main.zip
cd RooKie-main
```

### 2. 创建虚拟环境

```bash
# 使用 venv（Python 3.3+）
python -m venv venv

# 激活虚拟环境
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate

# 升级 pip
pip install --upgrade pip
```

### 3. 安装依赖

```bash
# 安装生产依赖
pip install -r requirements.txt

# 开发环境额外安装
pip install -r requirements-dev.txt
```

### 4. 环境配置

```bash
# 复制环境配置文件
cp .env.example .env

# 编辑配置文件
nano .env
```

**基础配置示例**:
```bash
# 基本设置
DJANGO_ENV=dev
SECRET_KEY=your-very-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# 数据库配置（开发环境使用SQLite）
DB_ENGINE=sqlite3
DB_NAME=db.sqlite3

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=logs/rookie.log
```

### 5. 初始化数据库

```bash
# 创建数据库迁移
python manage.py makemigrations

# 执行数据库迁移
python manage.py migrate

# 创建超级用户（可选）
python manage.py createsuperuser
```

### 6. 创建演示数据

```bash
# 运行演示数据脚本
python examples/admin_demo.py
```

### 7. 启动服务

```bash
# 启动开发服务器
python manage.py runserver

# 指定端口
python manage.py runserver 0.0.0.0:8000
```

### 8. 验证安装

访问以下URL验证安装：
- **管理后台**: http://127.0.0.1:8000/admin/
- **API文档**: http://127.0.0.1:8000/api/docs/
- **登录页面**: http://127.0.0.1:8000/login/

**默认登录信息**:
- 邮箱: `admin@example.com`
- 密码: `password123`

## 🐳 Docker 部署

### 开发环境

```bash
# 构建并启动服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f web

# 初始化数据库
docker-compose exec web python manage.py migrate
docker-compose exec web python examples/admin_demo.py
```

### 生产环境

```bash
# 设置环境变量
export SECRET_KEY="your-production-secret-key"
export DB_PASSWORD="your-database-password"
export ALLOWED_HOSTS="your-domain.com,www.your-domain.com"

# 启动生产服务
docker-compose -f docker-compose.prod.yml up -d

# 收集静态文件
docker-compose exec web python manage.py collectstatic --noinput

# 初始化数据库
docker-compose exec web python manage.py migrate
```

## 🗄️ 数据库配置

### SQLite（开发环境）

```python
# settings/dev.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### PostgreSQL（生产环境推荐）

```bash
# 安装 PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# 创建数据库和用户
sudo -u postgres psql
CREATE DATABASE rookie;
CREATE USER rookie WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE rookie TO rookie;
\q
```

```python
# settings/prod.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'rookie',
        'USER': 'rookie',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### MySQL（可选）

```bash
# 安装 MySQL
sudo apt-get install mysql-server

# 创建数据库
mysql -u root -p
CREATE DATABASE rookie CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'rookie'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON rookie.* TO 'rookie'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

```python
# settings/prod.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'rookie',
        'USER': 'rookie',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}
```

## 🔧 高级配置

### Redis 缓存配置

```bash
# 安装 Redis
sudo apt-get install redis-server

# 启动 Redis
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

```python
# settings/prod.py
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Session 存储到 Redis
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
```

### Nginx 反向代理

```nginx
# /etc/nginx/sites-available/rookie
server {
    listen 80;
    server_name your-domain.com;

    location /static/ {
        alias /path/to/rookie/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }

    location /media/ {
        alias /path/to/rookie/media/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# 启用站点
sudo ln -s /etc/nginx/sites-available/rookie /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### SSL/HTTPS 配置

```bash
# 使用 Let's Encrypt
sudo apt-get install certbot python3-certbot-nginx

# 获取 SSL 证书
sudo certbot --nginx -d your-domain.com

# 自动续期
sudo crontab -e
# 添加以下行
0 12 * * * /usr/bin/certbot renew --quiet
```

### Gunicorn 生产部署

```bash
# 安装 Gunicorn
pip install gunicorn

# 创建 Gunicorn 配置文件
# gunicorn.conf.py 已包含在项目中

# 启动 Gunicorn
gunicorn -c gunicorn.conf.py Rookie.wsgi:application
```

**Systemd 服务配置**:
```ini
# /etc/systemd/system/rookie.service
[Unit]
Description=Rookie Django Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/rookie
Environment="DJANGO_ENV=prod"
ExecStart=/path/to/rookie/venv/bin/gunicorn -c gunicorn.conf.py Rookie.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

```bash
# 启用服务
sudo systemctl daemon-reload
sudo systemctl enable rookie
sudo systemctl start rookie
sudo systemctl status rookie
```

## 🔐 第三方登录配置

### 钉钉登录配置

1. **获取钉钉应用凭证**
   - 登录钉钉开放平台
   - 创建企业内部应用
   - 获取 `corp_id`、`client_id`、`client_secret`

2. **配置回调地址**
   ```
   http://your-domain.com/api/users/third_party_callback/
   ```

3. **在管理后台配置**
   - 访问 `/admin/users/thirdpartyauthconfig/`
   - 添加钉钉配置：
   ```json
   {
     "corp_id": "your-corp-id",
     "client_id": "your-client-id", 
     "client_secret": "your-client-secret",
     "redirect_uri": "http://your-domain.com/api/users/third_party_callback/"
   }
   ```

### 企业微信配置

1. **获取企业微信应用信息**
   - 登录企业微信管理后台
   - 创建自建应用
   - 获取 `corp_id`、`agent_id`、`secret`

2. **配置可信域名**
   ```
   your-domain.com
   ```

3. **在管理后台配置**
   ```json
   {
     "corp_id": "your-corp-id",
     "agent_id": "your-agent-id",
     "secret": "your-secret",
     "redirect_uri": "http://your-domain.com/api/users/third_party_callback/"
   }
   ```

## 📊 监控配置

### 日志配置

```python
# settings/prod.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/django.log',
            'maxBytes': 1024*1024*10,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'INFO',
    },
}
```

### 健康检查

```python
# health_check/views.py
from django.http import JsonResponse
from django.db import connection

def health_check(request):
    try:
        # 检查数据库连接
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        return JsonResponse({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': timezone.now().isoformat()
        })
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': timezone.now().isoformat()
        }, status=500)
```

## 🔧 故障排除

### 常见问题

**1. 数据库连接错误**
```bash
# 检查数据库服务状态
sudo systemctl status postgresql

# 检查连接配置
python manage.py dbshell
```

**2. 静态文件无法加载**
```bash
# 收集静态文件
python manage.py collectstatic

# 检查 Nginx 配置
sudo nginx -t
```

**3. 第三方登录失败**
```bash
# 检查回调地址配置
# 确保域名和端口正确
# 检查防火墙设置
```

**4. 权限错误**
```bash
# 检查文件权限
sudo chown -R www-data:www-data /path/to/rookie
sudo chmod -R 755 /path/to/rookie
```

### 调试模式

```python
# settings/dev.py
DEBUG = True
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}
```

### 性能调试

```bash
# 安装调试工具
pip install django-debug-toolbar

# 启用调试工具栏
# settings/dev.py
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
INTERNAL_IPS = ['127.0.0.1']
```

## 📈 性能优化

### 数据库优化

```python
# 查询优化
users = User.objects.select_related('profile').prefetch_related('departments')

# 索引优化
class User(models.Model):
    email = models.EmailField(unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
```

### 缓存优化

```python
# 视图缓存
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # 缓存15分钟
def user_list(request):
    pass

# 模板缓存
{% load cache %}
{% cache 500 user_info user.id %}
    <!-- 用户信息模板 -->
{% endcache %}
```

### 静态文件优化

```python
# settings/prod.py
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# 启用 Gzip 压缩
MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    # ... 其他中间件
]
```

## 🔄 升级指南

### 版本升级

```bash
# 备份数据库
pg_dump rookie > backup_$(date +%Y%m%d_%H%M%S).sql

# 拉取最新代码
git pull origin main

# 更新依赖
pip install -r requirements.txt

# 执行数据库迁移
python manage.py migrate

# 收集静态文件
python manage.py collectstatic --noinput

# 重启服务
sudo systemctl restart rookie
```

### 回滚操作

```bash
# 回滚到指定版本
git checkout v1.0.0

# 回滚数据库迁移
python manage.py migrate users 0001

# 恢复数据库备份
psql rookie < backup_20240101_120000.sql
```

---

## 📞 获取帮助

如果在安装过程中遇到问题，可以通过以下方式获取帮助：

- 📧 **邮件支持**: support@rookie.com
- 💬 **社区讨论**: [GitHub Discussions](https://github.com/degary/RooKie/discussions)
- 🐛 **问题报告**: [GitHub Issues](https://github.com/degary/RooKie/issues)
- 📖 **详细文档**: [项目文档](docs/README.md)

---

**最后更新**: 2024-01-01  
**文档版本**: v1.0.0