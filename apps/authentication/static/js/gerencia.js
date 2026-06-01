document.addEventListener("DOMContentLoaded", function () {
    const filtro = document.getElementById("filtro-tabla");
    const filas = document.querySelectorAll("#tabla-gerencias tbody tr");

    filtro.addEventListener("keyup", function () {
      const texto = this.value.toLowerCase().trim();

      filas.forEach(function (fila) {
        // Ignora la fila del mensaje "No hay personas registradas"
        if (fila.querySelector(".tabla-vacia")) {
          return;
        }

        const nombre_gerencia = fila.children[1].textContent.toLowerCase();

        if (nombre_gerencia.includes(texto)) {
          fila.style.display = "";
        } else {
          fila.style.display = "none";
        }
      });
    });
});