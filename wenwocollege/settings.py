import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = '=m5dtfps#yt*)dn3d(jwda&of2g-f*x)_%=#hh!3bo^lz@_ju+'

DEBUG = True

ALLOWED_HOSTS = ['*']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "corsheaders",
    'wenwo.apps.ZhiyuConfig',
    "DjangoUeditor",
    "wenwo_auth",
    'blog',
    "common",
    "video_tutorial",
    "about",
    "activity",
    "topic",
    "mdeditor",
    "backoffice",
    "book",
    "wenworpc"
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = ()
  
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)
  
CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'api-token',
    'auth-token'
)


ROOT_URLCONF = 'wenwocollege.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['common/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'wenwo.views.global_variable',
            ],
        },
    },
]

WSGI_APPLICATION = 'wenwocollege.wsgi.application'

DATABASES = {
    'default': {
         #'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'wenwocollege',
        'USER': 'root',
        'PASSWORD': 'Zhiyu2019!',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4'
        },
    }
}

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

#配置Redis为Django缓存
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

MDEDITOR_CONFIGS = {
    'default': {
        'width': '100% ',
        'height': 500,
        'toolbar': ["undo", "redo", "|",
                    "bold", "del", "italic", "quote", "ucwords", "uppercase", "lowercase", "|",
                    "h1", "h2", "h3", "h5", "h6", "|",
                    "list-ul", "list-ol", "hr", "|",
                    "link", "reference-link", "image", "code", "preformatted-text", "code-block", "table", "datetime",
                    "emoji", "html-entities", "pagebreak", "goto-line", "|",
                    "help", "info",
                    "||", "preview", "watch", "fullscreen"],  # custom edit box toolbar
        'upload_image_formats': ["jpg", "jpeg", "gif", "png", "bmp", "webp"],  # image upload format type
        'image_folder': 'editor',  # image save the folder name
        'theme': 'default',  # edit box theme, dark / default
        'preview_theme': 'default',  # Preview area theme, dark / default
        'editor_theme': 'default',  # edit area theme, pastel-on-dark / default
        'toolbar_autofixed': True,  # Whether the toolbar capitals
        'search_replace': True,  # Whether to open the search for replacement
        'emoji': True,  # whether to open the expression function
        'tex': True,  # whether to open the tex chart function
        'flow_chart': True,  # whether to open the flow chart function
        'sequence': True,  # Whether to open the sequence diagram function
        'watch': True,  # Live preview
        'lineWrapping': False,  # lineWrapping
        'lineNumbers': False,  # lineNumbers
        'language': 'zh'  # zh / en / es
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            # 'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'format': '%(asctime)s %(name)s [%(module)s:%(levelname)s] %(message)s'
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            # 'level':'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            # 'stream': sys.stdout,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': True
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO'
    },
}

# 将session缓存在Redis中
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

SESSION_COOKIE_AGE = 60 * 60 * 12
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True


LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = True


STATIC_URL = '/data/wenwo/static/'
STATIC_ROOT = '/data/wenwo/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


ACCESSKEYID = 'LTAI4FsrVizgQCehFNZGBdJU'   # 短信验证吗 accessKeyId
ACCESSSECRET = 'prVvf6xYJoYTl99YZAlmbqBnZ6OaTG'  # 短信验证码 accessSecret
SIGNNAME = '问我学院'      # 短信验证码 SignName
TEMPLATECODE = 'SMS_183765549'  # 短信验证码 TemplateCode

QINIU_AK = "n_52Bt7SpmLuvnR7WfZJpWo5Q9h1SYWEFud6Aw5N"
QINIU_SK = "NgFTrIg5KPqzx5ZYaQLrClGqZr5CT_yAA04NzarA"
API_TOKEN = 'WenwoChaineyeChannel'
REST_API = "127.0.0.1"


GRPC_MAX_MESSAGE_LENGTH = 50 * 1024 * 1024
SCRAPY_GRPC_CHANNEL_URL = '10.10.8.200:50011'

try:
    from .local_settings import *
except ImportError:
    pass
