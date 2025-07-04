"""
基础配置文件
"""
from pathlib import Path
from django.templatetags.static import static
from django.urls import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-5at+5xnpe-%c=a@t^0o&5xh3s7+j5bs1!+fv1*2pmpx2z54iuq'

# Application definition
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Rookie.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Rookie.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 自定义用户模型
AUTH_USER_MODEL = 'users.User'

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}

# Jazzmin 配置
JAZZMIN_SETTINGS = {
    "site_title": "Rookie Admin",
    "site_header": "Rookie 管理后台",
    "site_brand": "Rookie",
    "site_logo": "images/logo.png",  # 侧边栏logo
    "login_logo": "images/logo.png",  # 登录页logo
    "site_logo_classes": "img-circle",  # logo样式：img-circle(圆形) 或 img-rounded(圆角)
    "site_icon": "images/favicon.ico",  # 浏览器图标
    "welcome_sign": "欢迎使用 Rookie 管理后台",
    "copyright": "Rookie Team",
    
    # 主题
    "theme": "flatly",
    "dark_mode_theme": "darkly",
    
    # 导航设置
    "show_sidebar": True,
    "navigation_expanded": True,
    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": [],
    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],
    
    # 图标设置
    "icons": {
        "users": "fas fa-users-cog",
        "users.User": "fas fa-user-circle",
        "users.UserProfile": "fas fa-id-card",
        "users.ThirdPartyAuthConfig": "fas fa-plug",
        "users.SystemModule": "fas fa-th-large",
        "users.ModulePermission": "fas fa-key",
        "auth": "fas fa-shield-alt",
        "auth.Group": "fas fa-users",
    },
    
    # 默认图标
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    
    # 表单样式
    "changeform_format": "horizontal_tabs",
    
    
    # 自定义链接
    "topmenu_links": [
        {"name": "首页", "url": "admin:index"},
        {"app": "users"},
    ],
}