
  document.addEventListener('DOMContentLoaded', function () {
    const inputFiltro = document.getElementById('filtro-tabla');
    const tabla = document.getElementById('tabla-usuarios');
    
    if (inputFiltro && tabla) {
      const filas = tabla.querySelectorAll('tbody tr');

      inputFiltro.addEventListener('keyup', function () {
        const textoBusqueda = this.value.toLowerCase().trim();

        filas.forEach(fila => {
          // Si es la fila de "No existen usuarios...", ignorar
          if (fila.querySelector('.tabla-vacia')) return;

          const celdas = fila.querySelectorAll('td');
          if (celdas.length >= 3) {
            // Columna 0: Colaborador / Nombre
            const nombre = celdas[0].textContent.toLowerCase();
            // Columna 2: Rol asignado
            const rol = celdas[2].textContent.toLowerCase();

            // Evalúa si el texto buscado coincide con Nombre O Rol
            if (nombre.includes(textoBusqueda) || rol.includes(textoBusqueda)) {
              fila.style.display = '';
            } else {
              fila.style.display = 'none';
            }
          }
        });
      });
    }
  });