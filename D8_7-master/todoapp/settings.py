import django_heroku
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECRET_KEY = os.environ.get('SECRET_KEY', 'please-set-secret-key-through-env')
SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['limitless-fortress-17369.herokuapp.com']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tasks.apps.TasksConfig',
]

ROOT_URLCONF = 'todoapp.urls'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'todoapp.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


LANGUAGE_CODE = 'ru-RU'


django_heroku.settings(locals())


def get_cache():
    environment_ready = all(
        os.environ.get(f'MEMCACHIER_{key}', False)
        for key in ['SERVERS', 'USERNAME', 'PASSWORD']
    )
    if not environment_ready:
        cache = {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}
    else:
        servers = os.environ['MEMCACHIER_SERVERS']
        username = os.environ['MEMCACHIER_USERNAME']
        password = os.environ['MEMCACHIER_PASSWORD']
        cache = {
            'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
            'TIMEOUT': 300,
            'LOCATION': servers,
            'OPTIONS': {
                'binary': True,
                'username': username,
                'password': password,
                'behaviors': {
                    # Enable faster IO
                    'no_block': True,
                    'tcp_nodelay': True,
                    # Keep connection alive
                    'tcp_keepalive': True,
                    # Timeout settings
                    'connect_timeout': 2000,  # ms
                    'send_timeout': 750 * 1000,  # us
                    'receive_timeout': 750 * 1000,  # us
                    '_poll_timeout': 2000,  # ms
                    # Better failover
                    'ketama': True,
                    'remove_failed': 1,
                    'retry_timeout': 2,
                    'dead_timeout': 30,
                }
            }
        }
    return {'default': cache}


CACHES = get_cache()
