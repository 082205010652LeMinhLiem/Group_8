document.addEventListener('DOMContentLoaded', function() {
    const registerButton = document.querySelector('button[type="submit"]');
    const remainingTickets = parseInt('{{ su_kien.so_luong_ve }}', 10);
    
    // Nếu không còn vé, vô hiệu hóa nút đăng ký và hiển thị thông báo
    if (remainingTickets <= 0) {
        registerButton.disabled = true;
        showAlert('alert-warning', 'Sự kiện đã hết vé! Vui lòng kiểm tra lại sau.');
    }

    function showAlert(alertClass, message) {
        const alertDiv = document.createElement('div');
        alertDiv.classList.add('alert', alertClass);
        alertDiv.textContent = message;
        document.querySelector('.event-details').appendChild(alertDiv);
    }
});
