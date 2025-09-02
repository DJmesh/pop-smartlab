"""
Django settings for app project — pronto para Render.

- Usa variáveis de ambiente: DJANGO_SECRET_KEY, DJANGO_DEBUG, DATABASE_URL.
- Ajusta ALLOWED_HOSTS/CSRF_TRUSTED_ORIGINS usando RENDER_EXTERNAL_HOSTNAME.
- WhiteNoise para servir estáticos em produção.
- dj_database_url para Postgres do Render (ou SQLite local).
"""

from pathlib import Path
import os
import dj_database_url

# -----------------------------------------------------
# Paths
# -----------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------------------------------------
# Básico / Segurança
# -----------------------------------------------------
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-only-change-me")
DEBUG = os.environ.get("DJANGO_DEBUG", "false").lower() == "true"

ALLOWED_HOSTS: list[str] = ["localhost", "127.0.0.1"]
RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Em muitos provedores (inclui Render) é útil honrar X-Forwarded-Proto
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# CSRF para produção no Render
# Render fornece somente o hostname (sem protocolo); montamos a origem HTTPS.
CSRF_TRUSTED_ORIGINS = []
if RENDER_EXTERNAL_HOSTNAME:
    CSRF_TRUSTED_ORIGINS.append(f"https://{RENDER_EXTERNAL_HOSTNAME}")

# -----------------------------------------------------
# Apps
# -----------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # apps do projeto
    "pages",
    "diagnostics",
]

# -----------------------------------------------------
# Middleware
# -----------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # WhiteNoise deve vir cedo (logo após SecurityMiddleware)
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# -----------------------------------------------------
# URLs / WSGI
# -----------------------------------------------------
ROOT_URLCONF = "app.urls"

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
            # Deixa {% static %} disponível sem precisar do {% load static %}
            "builtins": ["django.templatetags.static"],
        },
    },
]

WSGI_APPLICATION = "app.wsgi.application"

# -----------------------------------------------------
# Banco de Dados (SQLite local / Postgres via DATABASE_URL)
# -----------------------------------------------------
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        ssl_require=False,  # Render já força SSL no serviço de DB quando preciso
    )
}

# -----------------------------------------------------
# Senhas
# -----------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# -----------------------------------------------------
# i18n / TZ
# -----------------------------------------------------
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# -----------------------------------------------------
# Arquivos estáticos
# -----------------------------------------------------
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]  # seus assets (logo etc.) durante o dev
STATIC_ROOT = BASE_DIR / "staticfiles"    # destino do collectstatic em produção

# WhiteNoise: compressão + manifest para cache busting
STORAGES = {
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}

# -----------------------------------------------------
# Default PK
# -----------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# -----------------------------------------------------
# Logging (opcional mas útil em prod)
# -----------------------------------------------------
if not DEBUG:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "console": {"class": "logging.StreamHandler"},
        },
        "root": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "loggers": {
            "django.request": {"handlers": ["console"], "level": "WARNING", "propagate": False},
            "django.security": {"handlers": ["console"], "level": "WARNING", "propagate": False},
        },
    }
