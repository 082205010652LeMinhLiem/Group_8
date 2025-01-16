from django.db import models
from django.conf import settings  # Để sử dụng AUTH_USER_MODEL

class SuKien(models.Model):
    ten_su_kien = models.CharField(max_length=255)
    mo_ta = models.TextField()
    thoi_gian_bat_dau = models.DateTimeField()
    thoi_gian_ket_thuc = models.DateTimeField()
    dia_diem = models.CharField(max_length=255)
    gia_ve = models.DecimalField(max_digits=10, decimal_places=2)
    so_luong_ve = models.PositiveIntegerField()
    nguoi_tao = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='su_kien')
    image = models.ImageField(null=True, blank=True, default='default_image.jpg')


    def __str__(self):
        return self.ten_su_kien

class NguoiThamGia(models.Model):
    su_kien = models.ForeignKey(SuKien, on_delete=models.CASCADE, related_name='nguoi_tham_gia')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ngay_tham_gia = models.DateTimeField(auto_now_add=True)
    email_da_gui = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} tham gia {self.su_kien.ten_su_kien}'

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

    def __str__(self):
        return f'{self.loai_ve} ({self.su_kien.ten_su_kien})'

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

class SurveyResponse(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='responses')
    nguoi_tham_gia = models.ForeignKey(NguoiThamGia, on_delete=models.CASCADE, related_name='responses')
    phan_hoi = models.TextField()

    def __str__(self):
        return f'Phản hồi từ {self.nguoi_tham_gia.user.username} cho survey {self.survey.mo_ta}'
