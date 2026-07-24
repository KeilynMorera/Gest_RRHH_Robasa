
document.addEventListener('DOMContentLoaded', function () {
    const inputBusqueda = document.getElementById('buscarPremio');
    const tabla = document.getElementById('tablaPremios');

    if (inputBusqueda && tabla) {
      // Obtener todas las filas del tbody excluyendo la fila vacía
      const filas = tabla.querySelectorAll('tbody tr');

      inputBusqueda.addEventListener('input', function () {
        const termino = this.value.toLowerCase().trim();

        filas.forEach(fila => {
          // Obtener las celdas de Descripción (columna 2) y Categoría (columna 3)
          const celdaDescripcion = fila.cells[1];
          const celdaCategoria = fila.cells[2];

          // Validar que existan las celdas (evita errores con el tr de "sin registros")
          if (celdaDescripcion && celdaCategoria) {
            const textoDescripcion = celdaDescripcion.textContent.toLowerCase();
            const textoCategoria = celdaCategoria.textContent.toLowerCase();

            // Verificar si el término de búsqueda coincide con alguna de las dos columnas
            if (textoDescripcion.includes(termino) || textoCategoria.includes(termino)) {
              fila.style.display = '';
            } else {
              fila.style.display = 'none';
            }
          }
        });
      });
    }
});