document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('registerForm');

    form.addEventListener('submit', function (event) {
        const username = form.querySelector('#id_username').value.trim();
        const email = form.querySelector('#id_email').value.trim();
        const password1 = form.querySelector('#id_password1').value;
        const password2 = form.querySelector('#id_password2').value;

        // Elimina errores anteriores
        const existingErrors = form.querySelectorAll('.form-error');
        existingErrors.forEach(error => error.remove());

        let valid = true;

        // Validaciones básicas
        if (!username) {
            showError('El nombre de usuario es obligatorio.', '#id_username');
            valid = false;
        }

        if (!email) {
            showError('El correo electrónico es obligatorio.', '#id_email');
            valid = false;
        }

        if (!password1 || !password2) {
            showError('Ambas contraseñas son obligatorias.', '#id_password1');
            valid = false;
        }

        if (password1 && password2 && password1 !== password2) {
            showError('Las contraseñas no coinciden.', '#id_password2');
            valid = false;
        }

        if (!valid) {
            event.preventDefault(); // evita que se envíe el formulario
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
