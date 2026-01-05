from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

# Load .env for local development
load_dotenv()

# --------------------------
# BASE DIR
# --------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------------
# SECURITY
# --------------------------
SECRET_KEY = os.environ.get("SECRET_KEY", "fallback-secret-for-dev")
DEBUG = os.environ.get("DEBUG", "False") == "True"

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    ".railway.app",
    ".up.railway.app",
    "philharmonia-website-production.up.railway.app",
]

CSRF_TRUSTED_ORIGINS = [
    "https://philharmonia-website-production.up.railway.app",
    "https://*.railway.app",
]

# --------------------------
# HTTPS / SSL SETTINGS (Fix Google OAuth redirect)
# --------------------------
if os.environ.get("RAILWAY_ENVIRONMENT"):  # Only in production
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# --------------------------
# APPLICATION DEFINITION
# --------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",

    # Local apps
    "app.apps.AppConfig",

    # Third-party apps
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "storages",  # Cloudflare R2
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "app.middleware.LoginRedirectMiddleware",
]

ROOT_URLCONF = "HARMONY.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "HARMONY.wsgi.application"

# --------------------------
# DATABASE
# --------------------------
if os.environ.get("DATABASE_URL"):
    DATABASES = {
        "default": dj_database_url.config(
            default=os.environ.get("DATABASE_URL"),
            conn_max_age=600
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "Philharmonia_db",
            "USER": "Philharmonia_user",
            "PASSWORD": "Philharmonia",
            "HOST": "localhost",
            "PORT": "5432",
        }
    }

# --------------------------
# PASSWORD VALIDATORS
# --------------------------
AUTH_PASSWORD_VALIDATORS = []

# --------------------------
# INTERNATIONALIZATION
# --------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# --------------------------
# STATIC FILES
# --------------------------
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# --------------------------
# MEDIA FILES
# --------------------------
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "images"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --------------------------
# AUTHENTICATION
# --------------------------
AUTH_USER_MODEL = "app.CustomUser"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# Set SITE_ID to the production site ID
SITE_ID = 2  # Change if your production site has a different ID

LOGIN_REDIRECT_URL = "/user_home/"
LOGOUT_REDIRECT_URL = "/"
LOGIN_URL = "/login/"

# --------------------------
# ALLAUTH SETTINGS
# --------------------------
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]
ACCOUNT_EMAIL_VERIFICATION = "optional"
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_PREVENT_ENUMERATION = False

SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_VERIFICATION = "optional"
SOCIALACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_STORE_TOKENS = True
SOCIALACCOUNT_QUERY_EMAIL = True

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
            "secret": os.environ.get("GOOGLE_SECRET"),
            "key": ""
        },
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "online"},
        "OAUTH_PKCE_ENABLED": True,
    }
}

# --------------------------
# CLOUDFLARE R2 STORAGE (Production)
# --------------------------
R2_ACCOUNT_ID = os.environ.get("R2_ACCOUNT_ID")
R2_ACCESS_KEY_ID = os.environ.get("R2_ACCESS_KEY_ID")
R2_SECRET_ACCESS_KEY = os.environ.get("R2_SECRET_ACCESS_KEY")
R2_BUCKET_NAME = os.environ.get("R2_BUCKET_NAME", "philharmonia-media")

if os.environ.get("RAILWAY_ENVIRONMENT"):
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    AWS_ACCESS_KEY_ID = R2_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = R2_SECRET_ACCESS_KEY
    AWS_STORAGE_BUCKET_NAME = R2_BUCKET_NAME
    AWS_S3_ENDPOINT_URL = "https://0b418dde0bb4950435f6df4b43427951.r2.cloudflarestorage.com"
    AWS_S3_REGION_NAME = "auto"
    AWS_S3_CUSTOM_DOMAIN = "pub-a8c070b615064b4391ac33a8916b8b24.r2.dev"
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/"
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
    AWS_DEFAULT_ACL = "public-read"
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_FILE_OVERWRITE = False
