"""
shifts_project 用 Django 設定ファイル

Django 4.2.19 で 'django-admin startproject' により生成されたベース設定に、
プロジェクト固有のカスタマイズを加えている。

参考:
- https://docs.djangoproject.com/en/4.2/topics/settings/
- https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from datetime import timedelta

# =========================================
# パス設定
# =========================================

BASE_DIR = Path(__file__).resolve().parent.parent

# =========================================
# セキュリティ設定
# =========================================

# 本番環境では必ず秘密にすべきSECRET_KEY
SECRET_KEY = "django-insecure-(99hn_bor9^x&)tl=g_y3zr!-#23+zh_6u40lu&by&9+n!bxgf"

# デバッグモード（本番環境では必ずFalseにする）
DEBUG = True

# 許可するホスト
ALLOWED_HOSTS = []

# =========================================
# アプリケーション設定
# =========================================

INSTALLED_APPS = [
    # Django標準アプリ
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # サードパーティアプリ
    "rest_framework",
    "rest_framework.authtoken",
    "drf_spectacular",
    "django_extensions",
    "corsheaders",
    # 自作アプリ
    "user",
    "staff",
    "guest",
    "meal",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "shifts_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "shifts_project.wsgi.application"

# =========================================
# データベース設定
# =========================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
# =========================================
# パスワードバリデーション設定
# =========================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# =========================================
# 国際化設定
# =========================================

# 使用言語
LANGUAGE_CODE = "ja"

# タイムゾーン
TIME_ZONE = "Asia/Tokyo"

# 翻訳機能の使用
USE_I18N = True

# タイムゾーン対応 (USE_TZ=TrueだとUTC保存+ローカル表示)
USE_TZ = True

# =========================================
# 静的ファイル設定
# =========================================

STATIC_URL = "static/"

# =========================================
# デフォルト主キー型
# =========================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# =========================================
# カスタムユーザーモデル設定
# =========================================

AUTH_USER_MODEL = "user.User"

# =========================================
# DRF設定
# =========================================

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}

# =========================================
# drf-spectacular (OpenAPI/Swagger) 設定
# =========================================

SPECTACULAR_SETTINGS = {
    "TITLE": "出勤・食事・患者管理 API",
    "DESCRIPTION": "スタッフ出勤、利用者訪問、食事注文を一元管理するAPI",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SERVE_PERMISSIONS": ["rest_framework.permissions.AllowAny"],
    "COMPONENT_SPLIT_REQUEST": True,  # POST/PUTにリクエスト・レスポンスを分離表示
    "SWAGGER_UI_SETTINGS": {
        "docExpansion": "none",  # Swagger UIで初期展開しない
        "deepLinking": True,
        "defaultModelRendering": "example",
        "persistAuthorization": True,  # リロード後も認証情報を保持
    },
    "SECURITY": [{"BearerAuth": []}],  # Bearer認証方式
    "COMPONENTS": {
        "securitySchemes": {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            }
        }
    },
}

# =========================================
# SimpleJWT 設定
# =========================================

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),  # アクセストークンの有効期限
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),  # リフレッシュトークンの有効期限
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework.simplejwt.serializers.TokenRefreshSlidingSerializer",
}


CORS_ALLOW_ALL_ORIGINS = True


# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000", 
#     "http://127.0.0.1:8000", 
# ]