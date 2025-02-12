from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Trang chủ
    path('', views.home, name='home'),

    # Đăng nhập
    path('login/', views.login_view, name='login'),

    # Đăng ký người dùng
    path('register/', views.register_view, name='register'),

    # Chi tiết sự kiện
    path('sukien/<int:id>/', views.event_detail, name='event_detail'),

    # Tạo sự kiện mới
    path('create-event/', views.create_event, name='create_event'),

    # Đăng ký tham gia sự kiện
    path('register-event/<int:event_id>/', views.register_event, name='register_event'),  # Đổi id thành event_id để rõ ràng hơn

    # Các sự kiện của người dùng
    path('my-events/', views.my_events, name='my_events'),

    # Hiển thị các sự kiện sắp diễn ra
    path('upcoming-events/', views.upcoming_events, name='upcoming_events'),

    # Thông tin người tham gia sự kiện
    path('event-attendees/<int:id>/', views.event_attendees, name='event_attendees'),

    # Hồ sơ người dùng
    path('profile/', views.profile_view, name='profile'),

    # Đăng xuất
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Các trang thanh toán
    path('success/', views.success, name='success'),  # Sau khi thanh toán thành công
    path('cancel/', views.cancel, name='cancel'),  # Khi thanh toán bị hủy
]
