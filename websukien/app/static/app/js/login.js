// login.js

// Kiểm tra khi người dùng nhập liệu vào các trường
const form = document.querySelector('form');
const usernameInput = document.getElementById('id_username');
const passwordInput = document.getElementById('id_password');

form.addEventListener('submit', function(event) {
    if (usernameInput.value.trim() === '' || passwordInput.value.trim() === '') {
        alert('Vui lòng điền đầy đủ thông tin đăng nhập!');
        event.preventDefault(); // Ngừng gửi form nếu có trường trống
    }
});
