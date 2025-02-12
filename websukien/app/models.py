from django.db import models
from django.core.mail import send_mail
from django.conf import settings
import qrcode
from io import BytesIO
from django.contrib.auth.models import User
from django.core.files.base import ContentFile

class SuKien(models.Model):
    ten_su_kien = models.CharField(max_length=255)
    mo_ta = models.TextField()
    thoi_gian_bat_dau = models.DateTimeField()
    thoi_gian_ket_thuc = models.DateTimeField()
    dia_diem = models.CharField(max_length=255)
    gia_ve = models.DecimalField(max_digits=10, decimal_places=2)
    so_luong_ve = models.PositiveIntegerField()
    nguoi_tao = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='su_kien')
    hinh_anh = models.ImageField(upload_to='event_images/', blank=True, null=True)

    def __str__(self):
        return self.ten_su_kien

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)  # Thêm trường ảnh đại diện
    phone = models.CharField(max_length=20, blank=True, null=True)  # Thêm số điện thoại
    bio = models.TextField(blank=True, null=True)  # Thêm thông tin mô tả về bản thân

    def __str__(self):
        return self.user.username

class NguoiThamGia(models.Model):
    TRANG_THAI_THANH_TOAN = [
        ('pending', 'Chưa thanh toán'),
        ('paid', 'Đã thanh toán'),
        ('refunded', 'Hoàn tiền'),
    ]
    PHUONG_THUC_THANH_TOAN = [
        ('cash', 'Tiền mặt'),
        ('card', 'Thẻ tín dụng'),
        ('online', 'Thanh toán trực tuyến'),
    ]

    ten = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)  # Cho phép email là null
    so_dien_thoai = models.CharField(max_length=15, blank=True, null=True)
    su_kien = models.ForeignKey(SuKien, on_delete=models.CASCADE, related_name='nguoi_tham_gia')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ngay_tham_gia = models.DateTimeField(auto_now_add=True)
    email_da_gui = models.BooleanField(default=False)
    trang_thai_thanh_toan = models.CharField(max_length=20, choices=TRANG_THAI_THANH_TOAN, default='pending')
    phuong_thuc_thanh_toan = models.CharField(max_length=20, choices=PHUONG_THUC_THANH_TOAN, default='cash')
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.qr_code:
            qr = qrcode.make(f'{self.su_kien.id}-{self.user.id}')
            buffer = BytesIO()
            qr.save(buffer)
            self.qr_code.save(f'qr_{self.su_kien.id}_{self.user.id}.png', ContentFile(buffer.getvalue()), save=False)
        super().save(*args, **kwargs)
        # Gửi email thông báo khi người tham gia đăng ký sự kiện
        if not self.email_da_gui and self.email:  # Thêm điều kiện kiểm tra nếu có email
            self.send_registration_email()

    def send_registration_email(self):
        subject = f'Xác nhận đăng ký sự kiện {self.su_kien.ten_su_kien}'
        message = f'Chào {self.ten},\n\nCảm ơn bạn đã đăng ký tham gia sự kiện "{self.su_kien.ten_su_kien}".\n\nThông tin sự kiện:\n{self.su_kien.mo_ta}\n\nChúc bạn tham gia sự kiện thành công!'
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [self.email],
            fail_silently=False,
        )
        self.email_da_gui = True
        self.save()

    def __str__(self):
        return f'{self.ten} tham gia {self.su_kien.ten_su_kien}'

class DiaDiem(models.Model):
    ten_dia_diem = models.CharField(max_length=255)
    dia_chi = models.CharField(max_length=255)
    suc_chua = models.PositiveIntegerField()

    def __str__(self):
        return self.ten_dia_diem

class Ve(models.Model):
    su_kien = models.ForeignKey(SuKien, on_delete=models.CASCADE, related_name='ves')
    ma_ve = models.CharField(max_length=255)
    loai_ve = models.CharField(max_length=255)
    gia_ve = models.DecimalField(max_digits=10, decimal_places=2)
    so_luong = models.PositiveIntegerField()
    so_luong_da_ban = models.PositiveIntegerField(default=0)  # Số lượng vé đã bán
    ngay_bat_dau_ban_ve = models.DateTimeField(null=True, blank=True)
    ngay_ket_thuc_ban_ve = models.DateTimeField(null=True, blank=True)  
    nguoi_mua = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ves_mua', null=True, blank=True)
    nguoi_tham_gia = models.ForeignKey(User, null=True, on_delete=models.CASCADE) 

    def __str__(self):
        return f'{self.loai_ve} ({self.su_kien.ten_su_kien})'

    def ve_con_lai(self):
        return self.so_luong - self.so_luong_da_ban


class Sponsor(models.Model):
    ten_sponsor = models.CharField(max_length=255)
    su_kien = models.ManyToManyField(SuKien, related_name='sponsors')
    mo_ta = models.TextField()
    thong_tin_gian_hang = models.TextField()

    def __str__(self):
        return self.ten_sponsor

class Survey(models.Model):
    su_kien = models.ForeignKey(SuKien, on_delete=models.CASCADE, related_name='surveys')
    mo_ta = models.TextField()
    ngay_gui = models.DateTimeField(auto_now_add=True)
    da_gui = models.BooleanField(default=False)

    def __str__(self):
        return f'Survey for {self.su_kien.ten_su_kien}'

    def send_survey_email(self):
        if not self.da_gui:
            email_list = [nguoi.user.email for nguoi in self.su_kien.nguoi_tham_gia.all()]
            send_mail(
                f'Khảo sát cho sự kiện {self.su_kien.ten_su_kien}',
                self.mo_ta,
                settings.DEFAULT_FROM_EMAIL,
                email_list,
                fail_silently=False,
            )
            self.da_gui = True
            self.save()

class SurveyResponse(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='responses')
    nguoi_tham_gia = models.ForeignKey(NguoiThamGia, on_delete=models.CASCADE, related_name='responses')
    phan_hoi = models.TextField()

    def __str__(self):
        return f'Phản hồi từ {self.nguoi_tham_gia.ten} cho survey {self.survey.mo_ta}'


# Tạo tín hiệu để tự động tạo UserProfile khi người dùng được tạo
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
