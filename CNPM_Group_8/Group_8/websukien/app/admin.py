from django.contrib import admin
from .models import SuKien, NguoiThamGia, DiaDiem, Ve, Sponsor, Survey, SurveyResponse

@admin.register(SuKien)
class SuKienAdmin(admin.ModelAdmin):
    list_display = ('ten_su_kien', 'thoi_gian_bat_dau', 'thoi_gian_ket_thuc', 'dia_diem',)

@admin.register(NguoiThamGia)
class NguoiThamGiaAdmin(admin.ModelAdmin):
    list_display = ('su_kien', 'user', 'ngay_tham_gia',)

@admin.register(DiaDiem)
class DiaDiemAdmin(admin.ModelAdmin):
    list_display = ('ten_dia_diem', 'dia_chi', 'suc_chua',)

@admin.register(Ve)
class VeAdmin(admin.ModelAdmin):
    list_display = ('su_kien', 'ma_ve', 'loai_ve', 'gia_ve',)

@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ('ten_sponsor', 'mo_ta',)

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('su_kien', 'ngay_gui', 'da_gui',)

@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = ('survey', 'nguoi_tham_gia', 'phan_hoi',)
