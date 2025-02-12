from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import SuKien, UserProfile, NguoiThamGia

# Form đăng ký tài khoản người dùng
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    phone_number = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Số điện thoại'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tên đăng nhập'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mật khẩu'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Xác nhận mật khẩu'}),
        }

# Form đăng nhập người dùng
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tên đăng nhập'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mật khẩu'}))

# Form hồ sơ người dùng
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'phone', 'bio']  # Các trường bạn muốn cho phép người dùng chỉnh sửa

# Form tạo sự kiện
class SuKienForm(forms.ModelForm):
    class Meta:
        model = SuKien
        fields = ['ten_su_kien', 'mo_ta', 'thoi_gian_bat_dau', 'thoi_gian_ket_thuc', 'dia_diem', 'gia_ve', 'so_luong_ve']
        widgets = {
            'ten_su_kien': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tên sự kiện'}),
            'mo_ta': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Mô tả sự kiện'}),
            'thoi_gian_bat_dau': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'thoi_gian_ket_thuc': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'dia_diem': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Địa điểm tổ chức'}),
            'gia_ve': forms.NumberInput(attrs={'class': 'form-control'}),
            'so_luong_ve': forms.NumberInput(attrs={'class': 'form-control'}),
        }

# Form chỉnh sửa thông tin sự kiện
class UpdateEventForm(forms.ModelForm):
    class Meta:
        model = SuKien
        fields = ['ten_su_kien', 'mo_ta', 'thoi_gian_bat_dau', 'thoi_gian_ket_thuc', 'dia_diem', 'gia_ve', 'so_luong_ve']
        widgets = {
            'ten_su_kien': forms.TextInput(attrs={'class': 'form-control'}),
            'mo_ta': forms.Textarea(attrs={'class': 'form-control'}),
            'thoi_gian_bat_dau': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'thoi_gian_ket_thuc': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'dia_diem': forms.TextInput(attrs={'class': 'form-control'}),
            'gia_ve': forms.NumberInput(attrs={'class': 'form-control'}),
            'so_luong_ve': forms.NumberInput(attrs={'class': 'form-control'}),
        }

# Form đăng ký tham gia sự kiện
class EventRegistrationForm(forms.ModelForm):
    so_luong_ve = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Số lượng vé'}))

    class Meta:
        model = NguoiThamGia
        fields = ['so_luong_ve']

# Form thanh toán
class PaymentForm(forms.Form):
    PAYMENT_METHODS = [
        ('cash', 'Tiền mặt'),
        ('bank_transfer', 'Chuyển khoản'),
    ]
    payment_method = forms.ChoiceField(choices=PAYMENT_METHODS, label='Hình thức thanh toán', widget=forms.RadioSelect)
