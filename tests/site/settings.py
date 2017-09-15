import os


DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DATABASE_ENGINE',
                                 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('DATABASE_NAME', 'db.sqlite3'),
    }
}

ALLOWED_HOSTS = ['*']

SECRET_KEY = 'secretkey'

ROOT_URLCONF = 'tests.site.urls'

STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

USE_TZ = False

TESTS_ROOT = os.path.dirname(os.path.abspath(__file__))

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(TESTS_ROOT, 'site', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
            'debug': True,
        },
    },
]

MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_pdf',
    'tests.site',
]
