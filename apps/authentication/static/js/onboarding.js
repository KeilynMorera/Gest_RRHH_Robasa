document.addEventListener("DOMContentLoaded", function () {
        const inputFiltro = document.getElementById("filtro-actividades");
        const tabla = document.getElementById("tabla-actividades");

        if (inputFiltro && tabla) {
          inputFiltro.addEventListener("keyup", function () {
            // Convierte el texto buscado a minúsculas
            const terminoBusqueda = this.value.toLowerCase().trim();
            
            // Obtiene las filas del tbody descartando las del thead
            const filas = tabla.querySelectorAll("tbody tr");

            filas.forEach(function (fila) {
              // Verifica si es la fila de "No existen actividades..." (vacía)
              if (fila.querySelector(".tabla-vacia")) {
                return;
              }

              // Obtiene el texto de la primera columna (columna Actividad)
              const columnaActividad = fila.getElementsByTagName("td")[0];

              if (columnaActividad) {
                const textoActividad = columnaActividad.textContent || columnaActividad.innerText;

                // Compara el texto de la actividad con el término de búsqueda
                if (textoActividad.toLowerCase().indexOf(terminoBusqueda) > -1) {
                  fila.style.display = ""; // Muestra la fila
                } else {
                  fila.style.display = "none"; // Oculta la fila
                }
              }
            });
          });
        }
});