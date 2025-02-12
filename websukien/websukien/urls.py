from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Đường dẫn đến admin
    path('admin/', admin.site.urls),
    
    # Đường dẫn đến các URL của ứng dụng 'app'
    path('', include('app.urls')),  # Chỉ định các URL từ ứng dụng 'app'
]

# Cấu hình phục vụ các tệp media trong môi trường phát triển
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Cấu hình phục vụ các tệp static trong môi trường phát triển
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
