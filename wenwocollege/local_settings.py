DATABASES = {
    'default': {
         #'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'wenwocollege',
        'USER': 'root',
        'PASSWORD': 'Wenwo2020!',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4'
        },
    }
}