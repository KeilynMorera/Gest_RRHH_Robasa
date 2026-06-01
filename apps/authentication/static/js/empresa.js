document.addEventListener("DOMContentLoaded", function () {
    const filtro = document.getElementById("filtro-tabla");
    const filas = document.querySelectorAll("#tabla-empresas tbody tr");

    filtro.addEventListener("keyup", function () {
      const texto = this.value.toLowerCase().trim();

      filas.forEach(function (fila) {
        // Ignora la fila del mensaje "No hay personas registradas"
        if (fila.querySelector(".tabla-vacia")) {
          return;
        }

        const nombre_empresa = fila.children[1].textContent.toLowerCase();

        if (nombre_empresa.includes(texto)) {
          fila.style.display = "";
        } else {
          fila.style.display = "none";
        }
      });
    });
});