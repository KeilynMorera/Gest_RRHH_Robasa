/* ============================================================
   ARCHIVO: departamento.js
   MÓDULO: Registro y consulta de Departamentos
   ============================================================ */

/* ============================================================
   1. ESPERAR A QUE EL DOM ESTÉ COMPLETAMENTE CARGADO
   ============================================================ */

document.addEventListener("DOMContentLoaded", function () {
  /* ==========================================================
     2. OBTENER ELEMENTOS DEL HTML
     ========================================================== */

  // Campo de búsqueda de la tabla
  const filtroTabla = document.getElementById("filtro-tabla");

  // Tabla de departamentos
  const tablaDepartamentos = document.getElementById(
    "tabla-departamentos"
  );

  /* ==========================================================
     3. VALIDAR QUE LOS ELEMENTOS EXISTAN
     ========================================================== */

  // Si el buscador o la tabla no existen, detenemos el código
  if (!filtroTabla || !tablaDepartamentos) {
    console.warn(
      "No se encontró el buscador o la tabla de departamentos."
    );

    return;
  }

  /* ==========================================================
     4. OBTENER LAS FILAS DE LA TABLA
     ========================================================== */

  // Seleccionamos todas las filas del cuerpo de la tabla
  const filas = tablaDepartamentos.querySelectorAll(
    "tbody tr"
  );

  /* ==========================================================
     5. EVENTO DE BÚSQUEDA
     ========================================================== */

  filtroTabla.addEventListener("input", function () {
    // Obtener el texto escrito por el usuario
    const textoBuscado = filtroTabla.value
      .toLowerCase()
      .trim();

    /* ========================================================
       6. RECORRER CADA FILA DE LA TABLA
       ======================================================== */

    filas.forEach(function (fila) {
      // Obtener todas las celdas de la fila
      const celdas = fila.querySelectorAll("td");

      /*
       * Si la fila no tiene suficientes celdas,
       * probablemente corresponde al mensaje:
       *
       * "No existen departamentos registrados."
       *
       * En ese caso no hacemos nada.
       */
      if (celdas.length < 2) {
        return;
      }

      /* ======================================================
         7. OBTENER DATOS DE LA FILA
         ====================================================== */

      // Primera columna: Nombre del Departamento
      const nombreDepartamento = celdas[0].textContent
        .toLowerCase()
        .trim();

      // Segunda columna: Nombre de la Gerencia
      const nombreGerencia = celdas[1].textContent
        .toLowerCase()
        .trim();

      /* ======================================================
         8. COMPROBAR SI EXISTE COINCIDENCIA
         ====================================================== */

      /*
       * La fila se mostrará si el texto buscado aparece:
       *
       * - En el nombre del departamento
       * O
       * - En el nombre de la gerencia
       */

      const coincide =
        nombreDepartamento.includes(textoBuscado) ||
        nombreGerencia.includes(textoBuscado);

      /* ======================================================
         9. MOSTRAR U OCULTAR LA FILA
         ====================================================== */

      if (coincide) {
        // Mostrar la fila
        fila.style.display = "";
      } else {
        // Ocultar la fila
        fila.style.display = "none";
      }
    });
  });
});
