document.getElementById("recuperar-form").addEventListener("submit", function (e) {
  e.preventDefault();
  const email = document.getElementById("email").value;
  
  if (email) {
    alert("Se ha enviado un correo de recuperación a: " + email);
    // Aquí podrías usar fetch() para enviar los datos a Java backend
  } else {
    alert("Por favor ingresá tu correo electrónico.");
  }
});
