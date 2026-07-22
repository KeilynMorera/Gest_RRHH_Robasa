// ==========================================================================
// BUSCADOR DE EMPLEADOS EN LA TABLA DE SALDOS DE VACACIONES
// ==========================================================================

// Espera a que todo el contenido HTML esté cargado
document.addEventListener("DOMContentLoaded", function () {

  // ========================================================================
  // OBTENER ELEMENTOS DEL HTML
  // ========================================================================

  // Campo donde el usuario escribe el nombre que desea buscar
  const filtro = document.getElementById("filtro-saldo");

  // Tabla que contiene los registros de saldos
  const tabla = document.getElementById("tabla-saldos");

  // Verifica que existan ambos elementos antes de continuar
  if (!filtro || !tabla) {
    return;
  }

  // Obtiene todas las filas del cuerpo de la tabla
  const filas = tabla.querySelectorAll("tbody tr");

  // ========================================================================
  // EVENTO DE BÚSQUEDA
  // ========================================================================

  filtro.addEventListener("input", function () {

    // Obtiene el texto escrito por el usuario
    // y lo convierte a minúsculas para que la búsqueda
    // no distinga entre mayúsculas y minúsculas
    const textoBusqueda = filtro.value.toLowerCase().trim();

    // Recorre todas las filas de la tabla
    filas.forEach(function (fila) {

      // Obtiene todas las celdas de la fila
      const celdas = fila.querySelectorAll("td");

      // Si la fila no tiene celdas, no se procesa
      if (celdas.length === 0) {
        return;
      }

      // La columna del empleado es la segunda columna
      // Índice 0 = ID
      // Índice 1 = Empleado
      const nombreEmpleado = celdas[1].textContent
        .toLowerCase()
        .trim();

      // Comprueba si el nombre contiene el texto buscado
      if (nombreEmpleado.includes(textoBusqueda)) {

        // Muestra la fila si coincide
        fila.style.display = "";

      } else {

        // Oculta la fila si no coincide
        fila.style.display = "none";
      }
    });
  });
});