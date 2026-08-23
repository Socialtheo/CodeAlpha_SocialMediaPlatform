document.addEventListener('DOMContentLoaded', () => {

    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetTab = button.getAttribute('data-tab');

            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));

            button.classList.add('active');
            const targetElement = document.getElementById(targetTab);
            if (targetElement) {
                targetElement.classList.add('active');
            }
        });
    });

    const likeForms = document.querySelectorAll('.like-form');

    likeForms.forEach(form => {
        form.addEventListener('submit', (e) => {
            const button = form.querySelector('.btn-like');
            const countSpan = form.querySelector('.like-count');

            if (button && countSpan) {
                let currentLikes = parseInt(countSpan.textContent, 10);
                if (form.classList.contains('liked')) {
                    form.classList.remove('liked');
                    countSpan.textContent = currentLikes - 1;
                } else {
                    form.classList.add('liked');
                    countSpan.textContent = currentLikes + 1;
                }
            }
        });
    });

});