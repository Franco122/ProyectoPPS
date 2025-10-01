<script>
document.addEventListener("DOMContentLoaded", function () {
  // Botón "Agregar"
  document.querySelectorAll(".btn-success").forEach(function (btn) {
    btn.addEventListener("click", function () {
      // Buscar la fila del producto
      let fila = this.closest("tr");
      let cantidadCell = fila.querySelector("td:nth-child(5)"); // columna cantidad
      let cantidad = parseInt(cantidadCell.innerText);

      // Aumentar stock en +1
      cantidadCell.innerText = cantidad + 1;
    });
  });

  // Botón "Eliminar"
  document.querySelectorAll(".btn-danger").forEach(function (btn) {
    btn.addEventListener("click", function () {
      if (confirm("¿Seguro que deseas eliminar este producto?")) {
        let fila = this.closest("tr");
