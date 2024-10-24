from pathlib import Path
from datetime import timedelta,datetime
import logging
import os
from django.conf.global_settings import SESSION_FILE_PATH, SESSION_COOKIE_NAME

# AWS 配置
AWS_ACCESS_KEY_ID = 'AKIAXKPUZ3IJ5L47BSNI'
AWS_SECRET_ACCESS_KEY = 'xBqXQs5zwFJ0d0CzF+cx9hZGB0ctCujM4aqGH92+RW'
AWS_REGION = 'ap-southeast-2'

# Jenkins 配置
JENKINS_URL = 'http://127.0.0.1:8088'
JENKINS_USERNAME = 'admin'
JENKINS_PASSWORD = '123456'
BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-#^vq+d%*9dka^&!es8)t)1@y*to4d2*@5tl3b4sy@9x$sb+1nd'
DEBUG = True


ALLOWED_HOSTS = ["*"]


# Application definition
INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_yasg',
    'corsheaders',
    'awsresource',
    'deploy',
    'users',
]




# SimpleUI 的配置确保如以下所示
SIMPLEUI_HOME_TITLE = '自动化部署平台后台管理'  # 首页标题
SIMPLEUI_LOGIN_PAGE_TITLE = '自动化部署平台'  # 登录页面标题
SIMPLEUI_DEFAULT_TITLE = '自动化部署平台'  # 浏览器标签标题


# 中间件
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

# 路由配置对接
ROOT_URLCONF = 'core.urls'


SIMPLEUI_LOGO = ''  # 替换为你的自定义 logo
SIMPLEUI_HOME_INFO = False  # 隐藏主页信息
SIMPLEUI_ANALYSIS = False  # 关闭后台分析页面



# 模板配置
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# 启动配置对接
WSGI_APPLICATION = 'core.wsgi.application'


# 数据库配置对接
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
            'NAME': 'opsrun',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}



# 密码校验规则
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# REST_FRAMEWORK 框架配置 认证
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',  # 默认需要认证
    ),
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
}

# JWT配置
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=7200),   # 设置 access token 过期时间
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),     # 设置 refresh token 过期时间
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
}


# 文档swag对接JWT认证
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'JWT Authorization header using the Bearer scheme. Example: "Authorization: Bearer {token}"',
        }
    }
}




# CORS 允许所有源
CORS_ALLOW_ALL_ORIGINS = True


# 跨域允许范围
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:5173",
#     # 其他允许的源
# ]


# 日志配置
LOG_DIR = 'logs/'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOG_DIR, f'opsrun_{datetime.now().strftime("%Y-%m-%d")}.log'),
            'when': 'midnight',  # 每天切割
            'backupCount': 7,  # 保留最近7天的日志
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
logger = logging.getLogger(__name__)



SIMPLEUI_HOME_TITLE = '自动化部署平台' 
SIMPLEUI_LOGIN_PAGE_TITLE = '自动化部署平台' 