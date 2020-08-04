import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Custom additional apps
    'django.contrib.humanize',
    'bootstrap4',
    'social_django',
    'django_cleanup',
    'easy_thumbnails',
    'captcha',
    # 'rest_framework',
    # 'corsheaders',

    # Custom main apps
    'cinema.apps.CinemaConfig',
    'accounts',
    # 'api.apps.ApiConfig',
]

AUTH_USER_MODEL = 'accounts.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'beta_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'beta_project.wsgi.application'

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files (Images, Video)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

THUMBNAIL_ALIASES = {
    'cinema.Film.poster': {
        'index': {
            'size': (160, 200),
            'crop': 'smart',
            'autocrop': True,
        },
        'blu-ray_list': {
            'size': (245, 308),
            'crop': 'smart',
            'autocrop': True,
        },
        'film_list': {
            'size': (246, 317),
            'crop': 'smart',
            'autocrop': True,
        },
        'detail': {
            'size': (341, 444),
            'crop': 'smart',
            'autocrop': True,
        },
    },
    'cinema.News.news_detail_photo': {
        'slider_news': {
            'size': (557, 290),
            'crop': 'smart',
            'autocrop': True,
        },
        'box_news': {
            'size': (275, 155),
            'crop': 'smart',
            'autocrop': True,
        },
    },
    'cinema.News.news_feed_photo': {
        'news_list': {
            'size': (165, 245),
            'crop': 'smart',
            'autocrop': True,
        },
    },
    'cinema.CinemaPerson.avatar': {
        'person': {
            'size': (345, 450),
            'crop': 'smart',
            'autocrop': True,
        },
    },
}
THUMBNAIL_BASEDIR = 'thumbnails'

LOGOUT_REDIRECT_URL = 'cinema:index'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'yurii.borovenskyi@gmail.com'
EMAIL_HOST_PASSWORD = 'ACMilan1899Maldini'

AUTHENTICATION_BACKENDS = [
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'user_link']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
  'fields': 'id, name, email, picture.type(large), link'
}
SOCIAL_AUTH_FACEBOOK_EXTRA_DATA = [
    ('name', 'name'),
    ('email', 'email'),
    ('picture', 'picture'),
    ('link', 'profile_url'),
]
SOCIAL_AUTH_TWITTER_SCOPE = ['email', 'user']
SOCIAL_AUTH_TWITTER_PROFILE_EXTRA_PARAMS = {
  'fields': 'id, name, email'
}
SOCIAL_AUTH_GITHUB_SCOPE = ['email', 'user']
SOCIAL_AUTH_GITHUB_PROFILE_EXTRA_PARAMS = {
  'fields': 'id, name, email'
}

CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r'^/api/.*$'

# Local settings

try:
    from .local import *
except ImportError:
    pass
