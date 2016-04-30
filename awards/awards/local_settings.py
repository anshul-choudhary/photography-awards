

EMAIL_SITE_URL = 'localhost:8000'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'awards',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {'autocommit': True, }
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}



# DEBUG = False
