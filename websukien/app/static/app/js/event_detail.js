// event_detail.js

// Ví dụ: Thêm hiệu ứng nhẹ cho phần thông tin sự kiện
document.addEventListener("DOMContentLoaded", function() {
    const eventContainer = document.querySelector(".event-detail-container");
    if (eventContainer) {
        eventContainer.classList.add("fadeIn");
    }
});

// Sử dụng CSS để thêm hiệu ứng fadeIn
// .fadeIn {
//     opacity: 0;
//     animation: fadeInEffect 2s forwards;
// }

// @keyframes fadeInEffect {
//     to {
//         opacity: 1;
//     }
// }

// Xử lý sự kiện khi người dùng click vào nút đăng ký tham gia
const registerButton = document.querySelector(".btn-register");
if (registerButton) {
    registerButton.addEventListener("click", function(event) {
        alert("Bạn đã đăng ký tham gia sự kiện!");
    });
}
