from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.models import User
from .models import SuKien, NguoiThamGia, UserProfile, Ve
from .forms import SuKienForm, UserProfileForm
import stripe
from django.conf import settings
from datetime import datetime
from .models import SuKien

# Thiết lập API key cho Stripe từ settings
stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

def home_view(request):
    login_form = AuthenticationForm()
    register_form = UserCreationForm()
    return render(request, 'app/home.html', {'login_form': login_form, 'register_form': register_form})

# Trang chủ
def home(request):
    su_kiens = SuKien.objects.all()

    # Kiểm tra nếu người dùng đã đăng nhập
    user_profile = None
    if request.user.is_authenticated:
        user_profile, _ = UserProfile.objects.get_or_create(user=request.user)

    return render(request, 'app/home.html', {'su_kiens': su_kiens, 'user_profile': user_profile})

# Đăng nhập
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng.")
    else:
        form = AuthenticationForm()
    return render(request, 'app/login.html', {'form': form})

# Đăng ký
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Đăng ký thành công! Vui lòng đăng nhập.")
            return redirect('login')
        messages.error(request, "Đăng ký không thành công. Vui lòng thử lại.")
    else:
        form = UserCreationForm()
    return render(request, 'app/register.html', {'form': form})

# Tạo sự kiện
@login_required
def create_event(request):
    if request.method == 'POST':
        form = SuKienForm(request.POST)
        if form.is_valid():
            su_kien = form.save(commit=False)
            su_kien.nguoi_tao = request.user
            su_kien.save()
            # Gửi email thông báo tạo sự kiện
            send_mail(
                'Sự kiện của bạn đã được tạo thành công',
                f'Chúc mừng! Bạn đã tạo sự kiện: {su_kien.ten_su_kien}.',
                'from@example.com',  # Thay bằng email hệ thống
                [request.user.email],
                fail_silently=False,
            )
            messages.success(request, "Tạo sự kiện thành công!")
            return redirect('event_detail', su_kien.pk)
        messages.error(request, "Có lỗi xảy ra. Vui lòng kiểm tra lại thông tin.")
    else:
        form = SuKienForm()
    return render(request, 'app/create_event.html', {'form': form})

# Đăng ký tham gia sự kiện và thanh toán
@login_required
def register_event(request, event_id):
    su_kien = get_object_or_404(SuKien, id=event_id)

    if request.method == 'POST':
        # Lấy thông tin từ form
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        ticket_quantity = int(request.POST.get('ticket_quantity'))

        # Kiểm tra số lượng vé còn lại
        if su_kien.so_luong_ve >= ticket_quantity:
            # Tiến hành đăng ký (giả sử có một model để lưu thông tin đăng ký)
            su_kien.so_luong_ve -= ticket_quantity
            su_kien.save()
            
            # Hiển thị thông báo thành công
            messages.success(request, f'Đăng ký tham gia sự kiện "{su_kien.ten_su_kien}" thành công!')
        else:
            # Hiển thị thông báo thất bại
            messages.error(request, 'Sự kiện đã hết vé hoặc số lượng vé bạn yêu cầu vượt quá số vé còn lại.')

        return redirect('event_detail', su_kien.id)

    return render(request, 'app/register_event.html', {'su_kien': su_kien})


def event_detail(request, id):
    su_kien = get_object_or_404(SuKien, pk=id)
    so_luong_tham_gia = NguoiThamGia.objects.filter(su_kien=su_kien).count()  # Tính số người tham gia
    return render(request, 'app/event_detail.html', {'su_kien': su_kien, 'so_luong_tham_gia': so_luong_tham_gia})


# Danh sách sự kiện của tôi
@login_required
def my_events(request):
    su_kiens = SuKien.objects.filter(nguoi_tao=request.user)
    return render(request, 'app/my_events.html', {'su_kiens': su_kiens})

# Danh sách người tham gia sự kiện
@login_required
def event_attendees(request, id):
    su_kien = get_object_or_404(SuKien, pk=id, nguoi_tao=request.user)
    nguoi_tham_gia = su_kien.nguoi_tham_gia.all()
    return render(request, 'app/event_attendees.html', {'su_kien': su_kien, 'nguoi_tham_gia': nguoi_tham_gia})

# Hồ sơ cá nhân
@login_required
def profile_view(request):
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Cập nhật hồ sơ thành công!")
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'app/profile.html', {'form': form, 'user_profile': user_profile})

# Xử lý trang thành công thanh toán
def success(request):
    event_id = request.GET.get('event_id')
    user_id = request.GET.get('user_id')
    su_kien = get_object_or_404(SuKien, pk=event_id)
    user = get_object_or_404(User, pk=user_id)
    nguoi_tham_gia = NguoiThamGia.objects.get(user=user, su_kien=su_kien)
    
    # Cập nhật trạng thái thanh toán
    nguoi_tham_gia.trang_thai_thanh_toan = 'paid'
    nguoi_tham_gia.save()

    # Gửi email xác nhận thanh toán
    send_mail(
        'Thanh toán thành công',
        f'Chúc mừng! Bạn đã thanh toán thành công và đăng ký tham gia sự kiện {su_kien.ten_su_kien}.',
        'from@example.com',
        [user.email],
        fail_silently=False,
    )
    
    messages.success(request, "Thanh toán thành công! Bạn đã đăng ký tham gia sự kiện.")
    return redirect('home')

# Xử lý trang hủy thanh toán
def cancel(request):
    messages.error(request, "Thanh toán bị hủy. Vui lòng thử lại.")
    return redirect('home')

# Hiển thị các sự kiện sắp diễn ra
def upcoming_events(request):
    # Lọc các sự kiện mà thời gian diễn ra lớn hơn hoặc bằng hiện tại
    su_kiens_sap_dien_ra = SuKien.objects.filter(thoi_gian_bat_dau__gte=datetime.now()).order_by('thoi_gian_bat_dau')

    return render(request, 'app/upcoming_events.html', {'su_kiens_sap_dien_ra': su_kiens_sap_dien_ra})
