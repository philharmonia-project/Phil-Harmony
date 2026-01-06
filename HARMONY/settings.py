"""
Django settings for HARMONY project.
"""
import os
import dj_database_url
from pathlib import Path
import sys

# Load .env for local development
from dotenv import load_dotenv
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# =====================
# ENVIRONMENT DETECTION
# =====================
IS_RENDER = os.environ.get('RENDER', False)
IS_RAILWAY = os.environ.get('RAILWAY_ENVIRONMENT', False)
IS_PRODUCTION = IS_RENDER or IS_RAILWAY

# =====================
# SECURITY SETTINGS
# =====================
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY and IS_PRODUCTION:
    print("❌ ERROR: SECRET_KEY must be set in production!")
    sys.exit(1)

DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Render provides RENDER_EXTERNAL_HOSTNAME
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
ALLOWED_HOSTS = []

if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
    ALLOWED_HOSTS.append('*')  # Temporary for testing

# Add Railway hosts if needed
if IS_RAILWAY:
    ALLOWED_HOSTS.extend([
        "127.0.0.1",
        "localhost",
        ".railway.app",
        ".up.railway.app",
    ])

# Add localhost for development
if DEBUG:
    ALLOWED_HOSTS.extend(['localhost', '127.0.0.1'])

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = []
if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(f'https://{RENDER_EXTERNAL_HOSTNAME}')
    CSRF_TRUSTED_ORIGINS.append(f'http://{RENDER_EXTERNAL_HOSTNAME}')

# Add Railway origins if needed
if IS_RAILWAY:
    CSRF_TRUSTED_ORIGINS.extend([
        "https://*.railway.app",
    ])

# HTTPS Settings
if IS_PRODUCTION:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# =====================
# APPLICATION DEFINITION
# =====================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    
    # Your app
    'app.apps.AppConfig',
    
    # Third-party
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'storages',  # For Cloudflare R2 (MEDIA FILES ONLY)
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # For static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'HARMONY.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'HARMONY.wsgi.application'

# =====================
# DATABASE
# =====================
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            ssl_require=True
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# =====================
# PASSWORD VALIDATION
# =====================
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

# =====================
# INTERNATIONALIZATION
# =====================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# =====================
# STATIC FILES (CSS, JS) - SERVED BY DJANGO/WHITENOISE
# =====================
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# =====================
# MEDIA FILES (Images/Uploads) - SERVED BY CLOUDFLARE R2
# =====================
MEDIA_URL = '/media/'  # Default for development
MEDIA_ROOT = BASE_DIR / 'images'  # Local development only

# Cloudflare R2 Configuration
R2_ACCOUNT_ID = os.environ.get('R2_ACCOUNT_ID')
R2_ACCESS_KEY_ID = os.environ.get('R2_ACCESS_KEY_ID')
R2_SECRET_ACCESS_KEY = os.environ.get('R2_SECRET_ACCESS_KEY')
R2_BUCKET_NAME = os.environ.get('R2_BUCKET_NAME', 'phil-harmony')

# Check if R2 is configured
R2_CONFIGURED = all([
    R2_ACCOUNT_ID,
    R2_ACCESS_KEY_ID,
    R2_SECRET_ACCESS_KEY,
    R2_BUCKET_NAME
])

# =====================
# CLOUDFLARE R2 STORAGE (PRODUCTION ONLY)
# =====================
if IS_PRODUCTION and R2_CONFIGURED:
    print("✅ Production: Using Cloudflare R2 for MEDIA files only")
    
    # Configure R2 for MEDIA files only
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_ACCESS_KEY_ID = R2_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = R2_SECRET_ACCESS_KEY
    AWS_STORAGE_BUCKET_NAME = R2_BUCKET_NAME
    AWS_S3_ENDPOINT_URL = f'https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com'
    AWS_S3_REGION_NAME = 'auto'
    AWS_S3_CUSTOM_DOMAIN = f'pub-{R2_ACCOUNT_ID[:8]}.r2.dev'
    
    # IMPORTANT: Media files go to R2, static files stay with Django
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'
    
    # S3/R2 settings
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    AWS_DEFAULT_ACL = 'public-read'
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_FILE_OVERWRITE = False
    
    print(f"   Media URL: {MEDIA_URL}")
else:
    if IS_PRODUCTION:
        print("⚠️  Production: Using local storage (R2 not configured)")
    else:
        print("🛠️  Development: Using local file storage")

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =====================
# AUTHENTICATION
# =====================
AUTH_USER_MODEL = 'app.CustomUser'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Site ID - IMPORTANT: Change this if needed
SITE_ID = int(os.environ.get('SITE_ID', 1))

# Login/Logout URLs
LOGIN_REDIRECT_URL = '/user_home/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/login/'

# =====================
# ALLAUTH SETTINGS
# =====================
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_LOGOUT_ON_GET = True

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.environ.get('GOOGLE_CLIENT_ID'),
            'secret': os.environ.get('GOOGLE_SECRET'),
            'key': ''
        },
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
    }
}