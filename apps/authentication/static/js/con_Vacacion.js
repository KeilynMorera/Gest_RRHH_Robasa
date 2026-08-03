// ==========================================================================
// CONSULTA AJAX DE SALDOS Y FILTRO DE TABLA
// ==========================================================================

document.addEventListener("DOMContentLoaded", function () {

  // ========================================================================
  // 1. CÁLCULO AUTOMÁTICO DE DÍAS SEGÚN EMPLEADO Y AÑO
  // ========================================================================
  const selectEmpleado = document.getElementById("empleado");
  const inputAnio = document.getElementById("anio");
  const inputAcumulados = document.getElementById("dias_acumulados");
  const inputTomados = document.getElementById("dias_tomados");
  const inputDisponibles = document.getElementById("dias_disponibles");

  function recalcularDias() {
    if (!selectEmpleado) return;

    const empleadoId = selectEmpleado.value;
    // Si no hay año ingresado, toma el año actual
    const anio = inputAnio && inputAnio.value ? inputAnio.value : new Date().getFullYear();

    // Si deseleccionan el empleado, limpiamos los campos
    if (!empleadoId) {
      if (inputAcumulados) inputAcumulados.value = "";
      if (inputTomados) inputTomados.value = "";
      if (inputDisponibles) inputDisponibles.value = "";
      return;
    }

    // Construimos la URL enviando EMPLEADO Y AÑO
    const url = `/obtener-saldo-vacaciones/?empleado=${empleadoId}&anio=${anio}`;

    fetch(url, {
      headers: {
        "X-Requested-With": "XMLHttpRequest"
      }
    })
      .then(response => {
        if (!response.ok) {
          throw new Error("Error en la respuesta del servidor");
        }
        return response.json();
      })
      .then(data => {
        // Asignar los valores dinámicos
        if (inputAcumulados) inputAcumulados.value = data.acumulados ?? 0;
        if (inputTomados) inputTomados.value = data.tomados ?? 0;
        if (inputDisponibles) inputDisponibles.value = data.disponibles ?? 0;
      })
      .catch(error => {
        console.error("Error al obtener el saldo del empleado:", error);
      });
  }

  // Escuchar cambios en el selector de empleado
  if (selectEmpleado) {
    selectEmpleado.addEventListener("change", recalcularDias);
  }

  // Escuchar cambios o tipeo en el campo de Año
  if (inputAnio) {
    inputAnio.addEventListener("change", recalcularDias);
    inputAnio.addEventListener("input", recalcularDias);
  }


  // ========================================================================
  // 2. BUSCADOR EN LA TABLA DE SALDOS
  // ========================================================================
  const filtro = document.getElementById("filtro-saldo");
  const tabla = document.getElementById("tabla-saldos");

  if (filtro && tabla) {
    const filas = tabla.querySelectorAll("tbody tr");

    filtro.addEventListener("input", function () {
      const textoBusqueda = filtro.value.toLowerCase().trim();

      filas.forEach(function (fila) {
        const celdas = fila.querySelectorAll("td");

        if (celdas.length <= 1) return; // Ignora fila vacía

        // Columna Nombre del Empleado (Índice 1)
        const nombreEmpleado = celdas[1].textContent.toLowerCase().trim();

        if (nombreEmpleado.includes(textoBusqueda)) {
          fila.style.display = "";
        } else {
          fila.style.display = "none";
        }
      });
    });
  }
});