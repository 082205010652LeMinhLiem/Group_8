// profile.js

// Hiển thị ảnh đại diện ngay khi người dùng chọn file
document.addEventListener('DOMContentLoaded', function () {
    const avatarInput = document.getElementById('id_avatar');
    const avatarPreview = document.getElementById('avatar-preview');

    // Nếu đã có ảnh đại diện, hiển thị ngay
    if (avatarInput && avatarPreview) {
        avatarInput.addEventListener('change', function () {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    avatarPreview.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    }
});
