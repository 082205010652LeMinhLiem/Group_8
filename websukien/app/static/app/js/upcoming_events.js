// upcoming_events.js
document.addEventListener('DOMContentLoaded', function () {
    const eventCards = document.querySelectorAll('.event-card');
    
    eventCards.forEach(card => {
        card.addEventListener('mouseenter', function () {
            card.style.boxShadow = '0px 4px 8px rgba(0, 0, 0, 0.1)';
        });
        card.addEventListener('mouseleave', function () {
            card.style.boxShadow = 'none';
        });
    });
});
