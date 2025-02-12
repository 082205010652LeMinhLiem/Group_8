from django.contrib import admin
from .models import SuKien, NguoiThamGia, DiaDiem, Ve, Sponsor, Survey, SurveyResponse

# Đăng ký mô hình SuKien
@admin.register(SuKien)
class SuKienAdmin(admin.ModelAdmin):
    list_display = ('ten_su_kien', 'thoi_gian_bat_dau', 'thoi_gian_ket_thuc', 'dia_diem', 'nguoi_tao', 'so_luong_ve', 'get_image')  # Thêm 'get_image' để hiển thị hình ảnh
    search_fields = ('ten_su_kien', 'dia_diem', 'nguoi_tao__username')
    list_filter = ('thoi_gian_bat_dau', 'nguoi_tao', 'dia_diem')
    list_editable = ('so_luong_ve',)
    ordering = ('-thoi_gian_bat_dau',)
    fieldsets = (
        ('Thông tin chung', {
            'fields': ('ten_su_kien', 'mo_ta', 'nguoi_tao', 'hinh_anh')  # Thêm trường 'hinh_anh' vào
        }),
        ('Thời gian và địa điểm', {
            'fields': ('thoi_gian_bat_dau', 'thoi_gian_ket_thuc', 'dia_diem')
        }),
        ('Vé và số lượng', {
            'fields': ('gia_ve', 'so_luong_ve')
        }),
    )
    date_hierarchy = 'thoi_gian_bat_dau'
    list_select_related = ('nguoi_tao', 'dia_diem')

    # Hàm để hiển thị hình ảnh trong bảng
    def get_image(self, obj):
        if obj.hinh_anh:
            return f'<img src="{obj.hinh_anh.url}" width="100" height="100" />'  # Chỉ hiển thị ảnh với kích thước nhỏ
        return 'No Image'
    get_image.allow_tags = True  # Cho phép HTML trong bảng
    get_image.short_description = 'Hình ảnh'

# Đăng ký mô hình NguoiThamGia
@admin.register(NguoiThamGia)
class NguoiThamGiaAdmin(admin.ModelAdmin):
    list_display = ('su_kien', 'user', 'ngay_tham_gia', 'email_da_gui')
    search_fields = ('su_kien__ten_su_kien', 'user__username')  # Tìm kiếm theo tên sự kiện và tên người dùng
    list_filter = ('su_kien', 'ngay_tham_gia', 'email_da_gui')  # Lọc theo sự kiện, ngày tham gia, và trạng thái email
    date_hierarchy = 'ngay_tham_gia'  # Hiển thị thanh điều hướng theo ngày tham gia

# Đăng ký mô hình DiaDiem
@admin.register(DiaDiem)
class DiaDiemAdmin(admin.ModelAdmin):
    list_display = ('ten_dia_diem', 'dia_chi', 'suc_chua')
    search_fields = ('ten_dia_diem', 'dia_chi')  # Tìm kiếm theo tên địa điểm và địa chỉ
    list_filter = ('suc_chua',)  # Lọc theo sức chứa

# Đăng ký mô hình Ve
@admin.register(Ve)
class VeAdmin(admin.ModelAdmin):
    list_display = ('su_kien', 'ma_ve', 'loai_ve', 'gia_ve', 'so_luong')
    search_fields = ('su_kien__ten_su_kien', 'ma_ve')  # Tìm kiếm theo tên sự kiện và mã vé
    list_filter = ('su_kien', 'loai_ve')  # Lọc theo sự kiện và loại vé
    list_editable = ('gia_ve', 'so_luong')  # Cho phép chỉnh sửa trực tiếp giá vé và số lượng

# Đăng ký mô hình Sponsor
@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ('ten_sponsor', 'mo_ta')
    search_fields = ('ten_sponsor',)  # Tìm kiếm theo tên sponsor
    filter_horizontal = ('su_kien',)  # Cho phép chọn nhiều sự kiện một cách dễ dàng
    fieldsets = (
        ('Thông tin chung', {
            'fields': ('ten_sponsor', 'mo_ta')
        }),
        ('Sự kiện liên quan', {
            'fields': ('su_kien',)
        }),
    )

# Đăng ký mô hình Survey
@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('su_kien', 'ngay_gui', 'da_gui')
    search_fields = ('su_kien__ten_su_kien',)  # Tìm kiếm theo tên sự kiện
    list_filter = ('su_kien', 'da_gui')  # Lọc theo sự kiện và trạng thái gửi
    actions = ['mark_as_sent']  # Thêm hành động tùy chỉnh

    # Hành động tùy chỉnh: Đánh dấu là đã gửi
    def mark_as_sent(self, request, queryset):
        queryset.update(da_gui=True)
    mark_as_sent.short_description = "Đánh dấu là đã gửi"

# Đăng ký mô hình SurveyResponse
@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = ('survey', 'nguoi_tham_gia', 'phan_hoi')
    search_fields = ('survey__su_kien__ten_su_kien', 'nguoi_tham_gia__user__username')  # Tìm kiếm theo tên sự kiện và tên người tham gia
    list_filter = ('survey',)  # Lọc theo survey
    readonly_fields = ('nguoi_tham_gia', 'survey')  # Chỉ cho phép xem, không chỉnh sửa