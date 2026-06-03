document.addEventListener("DOMContentLoaded", function () {

  const filtro = document.getElementById("filtro-tabla");
  const filas  = document.querySelectorAll("#tabla-compensaciones tbody tr");

  if (!filtro) return; // Previene error si el elemento no existe en la página

  filtro.addEventListener("keyup", function () {
    const texto = this.value.toLowerCase().trim();

    filas.forEach(function (fila) {

      // Ignora la fila del mensaje "No existen compensaciones registradas"
      if (fila.querySelector(".tabla-vacia")) return;

      // Columnas a buscar:
      // [0] ID  [1] Puesto  [2] Salario Bruto  [3] Salario Neto  [4] Vigencia
      const puesto   = fila.children[1]?.textContent.toLowerCase() ?? "";
      const bruto    = fila.children[2]?.textContent.toLowerCase() ?? "";
      const neto     = fila.children[3]?.textContent.toLowerCase() ?? "";
      const vigencia = fila.children[4]?.textContent.toLowerCase() ?? "";

      // Muestra la fila si el texto coincide con CUALQUIERA de las columnas
      const coincide = puesto.includes(texto)   ||
                       bruto.includes(texto)    ||
                       neto.includes(texto)     ||
                       vigencia.includes(texto);

      fila.style.display = coincide ? "" : "none";
    });

    // Si todas las filas están ocultas, muestra un mensaje vacío dinámico
    const visibles = [...filas].filter(f =>
      !f.querySelector(".tabla-vacia") && f.style.display !== "none"
    );

    // Remueve mensaje dinámico anterior si existe
    const mensajeDinamico = document.getElementById("sin-resultados");
    if (mensajeDinamico) mensajeDinamico.remove();

    // Inserta mensaje si no hay resultados y hay texto escrito
    if (visibles.length === 0 && texto !== "") {
      const tbody = document.querySelector("#tabla-compensaciones tbody");
      const fila  = document.createElement("tr");
      fila.id     = "sin-resultados";
      fila.innerHTML = `
        <td colspan="6" class="tabla-vacia">
          <i class="fas fa-magnifying-glass"></i>
          No se encontraron compensaciones para "<strong>${texto}</strong>"
        </td>`;
      tbody.appendChild(fila);
    }
  });

});