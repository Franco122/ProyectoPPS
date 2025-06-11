document.getElementById("registerForm").addEventListener("submit", function(e) {
  e.preventDefault();

  const password = document.getElementById("password").value;
  const repeatPassword = document.getElementById("repeatPassword").value;

  if (password !== repeatPassword) {
    alert("Las contraseñas no coinciden.");
    return;
  }

  const data = {
    name: document.getElementById("name").value,
    email: document.getElementById("email").value,
    password: password
  };

  fetch("http://localhost:8080/api/usuarios", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  })
  .then(response => {
    if (response.ok) {
      alert("Usuario registrado con éxito");
    } else {
      alert("Error al registrar usuario");
    }
  })
  .catch(error => {
    alert("Error de conexión: " + error);
  });
});
