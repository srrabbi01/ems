from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-)%+s+4!d-gevfk*z+hi_(e@2#yjizg94=0!veh0#8@h2x-@0br'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1','*']


# Application definition

INSTALLED_APPS = [
    'jet.dashboard',
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'app_dashboard',
    'api',
    'app_auth',
    'app_index',
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
]

ROOT_URLCONF = 'ems.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'app_dashboard.custom_context_processor.invoiceform',
                'app_dashboard.custom_context_processor.get_mdod',
            ],
        },
    },
]

WSGI_APPLICATION = 'ems.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
from .config import *

DATABASES = DATABASES_SQLITE3


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
from .config import *

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

if not DEBUG:
    MEDIA_ROOT = ROOT / DOMAIN_ROOT / 'mediafiles'
    MEDIA_URL = '/mediafiles/'

else:
    MEDIA_ROOT = BASE_DIR / 'mediafiles'
    MEDIA_URL = '/media/'
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


EMAIL_HOST = 'mail.excellentworld.xyz'
EMAIL_HOST_USER = 'info@ems.excellentworld.xyz'
EMAIL_HOST_PASSWORD = 'SJ!20v.1vE3vuH'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = 'Ems <info@ems.excellentworld.xyz>'


JET_THEMES = [
    {
        'theme': 'default', # theme folder name
        'color': '#47bac1', # color of the theme's button in user menu
        'title': 'Default' # theme title
    },
    {
        'theme': 'green',
        'color': '#44b78b',
        'title': 'Green'
    },
    {
        'theme': 'light-green',
        'color': '#2faa60',
        'title': 'Light Green'
    },
    {
        'theme': 'light-violet',
        'color': '#a464c4',
        'title': 'Light Violet'
    },
    {
        'theme': 'light-blue',
        'color': '#5EADDE',
        'title': 'Light Blue'
    },
    {
        'theme': 'light-gray',
        'color': '#222',
        'title': 'Light Gray'
    }
]

JET_SIDE_MENU_COMPACT = True

X_FRAME_OPTIONS = 'SAMEORIGIN'


JET_SIDE_MENU_ITEMS = [  # A list of application or custom item dicts
    {'label': ('Ems Functionality'), 'items': [
        {'name': 'app_dashboard.userregistration','label': ('Created Accounts')},
        {'name': 'app_dashboard.servicecategory','label': ('Cost Category')},
        {'name': 'app_dashboard.servicerequest','label': ('Requested Services')},
        {'name': 'app_dashboard.invoice','label': ('Invoice List')},
        {'name': 'app_dashboard.message','label': ('Message List')},
        {'name': 'app_dashboard.tempservicerequest','label': ('Temp Service List')},
        {'name': 'app_dashboard.review','label': ('Reviews')},
        {'name': 'app_dashboard.customerpayment','label': ('Customer Payment')},
        {'name': 'app_dashboard.technicianpayment','label': ('Technician Payment')},
        {'name': 'app_dashboard.contact','label': ('Contact')},
    ]},
    {'label': ('Area Data'), 'items': [
        {'name': 'api.country','label': ('Countrys')},
        {'name': 'api.division','label': ('Divisions')},
        {'name': 'api.district','label': ('Districts')},
        {'name': 'api.upazila','label': ('Upazilas')},
    ]},
    {'label': ('user accounts and groups'),'app_label':'auth', 'items': [
        {'name': 'auth.user'},
        {'name': 'auth.group'},
    ]},
]
