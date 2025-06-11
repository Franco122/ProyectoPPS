document.getElementById("loginForm").addEventListener("submit", function (e) {
  e.preventDefault();
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  // Ejemplo simple (simular conexión al back-end)
  if (email === "admin@stopmarket.com" && password === "1234") {
    alert("Inicio de sesión exitoso");
  } else {
    alert("Correo o contraseña incorrectos");
  }
});
