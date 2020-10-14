import os
import dotenv

# SECURITY WARNING: keep the secret key used in production secret!

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
START_SETTING = os.environ.get("PYTHON_ENV")

if START_SETTING == "PRODUCTION":
    DEBUG = True
    ALLOWED_HOSTS = ["https://shtern-olymp.ru/", "shtern-olymp.ru"]
else:
    DEBUG = True
    ALLOWED_HOSTS = []

DATABASES = {
            'default':
                {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
                    'USER': os.environ.get("USER"),
                    'PASSWORD': os.environ.get("PASSWORD"),
                    'HOST': 'localhost',
                    'PORT': '',
                }
            }


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sore',
    'widget_tweaks',
    'whitenoise',
    'tinymce'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
]

ROOT_URLCONF = 'sternadditional.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = 'sternadditional.wsgi.application'


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    }
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "staticfiles")

# Payment olympiad
SECRET_KEY_PAYMENT = os.environ.get('SECRET_KEY_PAYMENT')
PRICE = str(10)
DESC = 'Оплата за олимпиаду'
MERCHANT_ID = os.environ.get('MERCHANT_ID')

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST = 'smtp.beget.com'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

# Text for greetings
REGISTRATION_TEXT = "Поздравляем Вас с регистрацией на олимпиаду! \nНиже представлены логин и пароль от Вашего аккаунта. Просим, не сообщать никому данные. \nВаш логин: {} \nВаш пароль: {} \nЛюбые возникшие вопросы Вы можете задать в чате технической поддержки на сайте.\nУспешного написания олимпиады!\nС уважением, Школа Точных Наук 'Штерн'!"
