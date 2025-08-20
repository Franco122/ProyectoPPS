document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('loginForm');

    form.addEventListener('submit', function (event) {
        const username = form.querySelector('#id_username').value.trim();
        const password = form.querySelector('#id_password').value.trim();

        // Elimina errores anteriores
        const existingErrors = form.querySelectorAll('.form-error');
        existingErrors.forEach(error => error.remove());

        let valid = true;

        if (!username) {
            showError('El nombre de usuario es obligatorio.', '#id_username');
            valid = false;
        }

        if (!password) {
            showError('La contraseña es obligatoria.', '#id_password');
            valid = false;
        }

        if (!valid) {
            event.preventDefault();
        }
    });

    function showError(message, selector) {
        const input = document.querySelector(selector);
        const error = document.createElement('div');
        error.className = 'form-error';
        error.style.color = 'red';
        error.style.fontSize = '14px';
        error.style.marginTop = '4px';
        error.textContent = message;
        input.parentNode.insertBefore(error, input.nextSibling);
    }
});
