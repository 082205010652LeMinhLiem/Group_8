// register.js

// Kiểm tra sự phù hợp của mật khẩu khi người dùng nhập
const password1 = document.getElementById('id_password1');
const password2 = document.getElementById('id_password2');
const form = document.querySelector('form');

form.addEventListener('submit', function(event) {
    if (password1.value !== password2.value) {
        alert('Mật khẩu và mật khẩu xác nhận không khớp!');
        event.preventDefault();
    }
});

// Thêm hiệu ứng hiển thị lỗi nếu mật khẩu không khớp
password2.addEventListener('input', function() {
    if (password1.value !== password2.value) {
        password2.setCustomValidity('Mật khẩu xác nhận không khớp');
    } else {
        password2.setCustomValidity('');
    }
});
