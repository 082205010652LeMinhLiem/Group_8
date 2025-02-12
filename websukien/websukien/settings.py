import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Cấu hình bảo mật và các cài đặt nhanh
SECRET_KEY = 'django-insecure-b_8_ff5+od&xn7b*1*!@(u*(tjppq=_omgk=tqv@mg#z9en%tv'
DEBUG = True
ALLOWED_HOSTS = ['*']

# Cài đặt ứng dụng
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',  # Đảm bảo ứng dụng 'app' của bạn được liệt kê
    'django.contrib.sites',
]

# Middleware và các cấu hình khác
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'websukien.urls'

# Cấu hình templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'app/templates')],  # Thêm thư mục templates của app
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

WSGI_APPLICATION = 'websukien.wsgi.application'

# Cấu hình database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # Dùng SQLite cho phát triển
    }
}

# Xác thực mật khẩu
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Cấu hình quốc tế hóa và múi giờ
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Cấu hình Static files (CSS, JS, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'app/static')]  # Đảm bảo đường dẫn này đúng cho thư mục static

# Cấu hình Media files (hình ảnh, video...)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Thư mục lưu trữ tất cả các tệp media

# Cấu hình email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'liemliem910@gmail.com'
EMAIL_HOST_PASSWORD = 'LML_2005'
DEFAULT_FROM_EMAIL = 'no-reply@websukien.com'

# Cấu hình Sites Framework
SITE_ID = 2

# Cấu hình Stripe
STRIPE_TEST_SECRET_KEY = 'your_test_secret_key'  # Thay 'your_test_secret_key' bằng khóa thực tế của bạn
STRIPE_TEST_PUBLIC_KEY = 'your_test_public_key'  # Thay 'your_test_public_key' bằng khóa công khai thực tế của bạn

# Cấu hình Momo
MOMO_PARTNER_CODE = 'your_partner_code'  # Mã đối tác Momo
MOMO_ACCESS_KEY = 'your_access_key'  # Access Key từ Momo
MOMO_SECRET_KEY = 'your_secret_key'  # Secret Key từ Momo
MOMO_ORDER_TYPE = 'payment'  # Loại đơn hàng
MOMO_RETURN_URL = 'your_return_url'  # URL để trả về sau khi thanh toán
MOMO_NOTIFY_URL = 'your_notify_url'  # URL để nhận thông báo từ Momo

# Cấu hình cho static và media trong môi trường phát triển
from django.conf import settings
from django.conf.urls.static import static

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

# Cấu hình URL
urlpatterns = [
    # Các URL của bạn
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
