<script>
  let totalVirtual = 0;

  const formVirtual = document.getElementById("formVirtual");
  const listaVirtual = document.getElementById("listaVirtual");
  const totalVirtualSpan = document.getElementById("totalVirtual");

  formVirtual.addEventListener("submit", function (e) {
    e.preventDefault();

    const monto = parseFloat(document.getElementById("montoVirtual").value);
    const desc = document.getElementById("descVirtual").value;

    if (isNaN(monto) || desc.trim() === "") return;

    // Crear item de la lista
    const li = document.createElement("li");
    li.className = "list-group-item d-flex justify-content-between align-items-center";
    li.innerHTML = `
      <div>
        <strong>${new Date().toLocaleString()}</strong> - $${monto.toFixed(2)}
        <span class="text-muted">(${desc})</span>
      </div>
      <button class="btn btn-danger btn-sm">🗑️</button>
    `;

    // Botón eliminar
    li.querySelector("button").addEventListener("click", () => {
      listaVirtual.removeChild(li);
      totalVirtual -= monto;
      totalVirtualSpan.textContent = totalVirtual.toFixed(2);
    });

    // Agregar a la lista
    listaVirtual.prepend(li);

    // Actualizar total
    totalVirtual += monto;
    totalVirtualSpan.textContent = totalVirtual.toFixed(2);

    // Reset form
    formVirtual.reset();
  });
</script>