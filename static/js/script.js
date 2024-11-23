document.addEventListener('DOMContentLoaded', function () {
    // Пример для формы логина
    const loginForm = document.querySelector('#loginForm');
    const usernameInput = document.querySelector('#username');
    const passwordInput = document.querySelector('#password');

    loginForm.addEventListener('submit', function (e) {
        // Проверка на пустые поля перед отправкой
        if (usernameInput.value.trim() === '' || passwordInput.value.trim() === '') {
            e.preventDefault();  // Отменяем отправку формы
            alert('Please fill in all fields.');
        }
    });

    // Пример для формы регистрации
    const registerForm = document.querySelector('#registerForm');
    registerForm.addEventListener('submit', function (e) {
        const password = document.querySelector('#password').value;
        const confirmPassword = document.querySelector('#confirm_password').value;
        if (password !== confirmPassword) {
            e.preventDefault();
            alert('Passwords do not match!');
        }
    });
});
