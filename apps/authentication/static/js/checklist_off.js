
document.addEventListener('DOMContentLoaded', function () {
    const inputFiltro = document.getElementById('filtro-tabla');
    const tabla = document.getElementById('tabla-offboarding');

    if (!inputFiltro || !tabla) return;

    // Obtenemos únicamente las filas del cuerpo de la tabla
    const filas = tabla.querySelectorAll('tbody tr');

    inputFiltro.addEventListener('keyup', function () {
      const textoBusqueda = this.value.toLowerCase().trim();

      filas.forEach(function (fila) {
        // Ignorar la fila de "No existen procesos..." si no hay registros
        if (fila.querySelector('.tabla-vacia')) return;

        // Seleccionamos las celdas de ID Offboarding (col 0), Colaborador (col 1) y Causa (col 2)
        const idOffboarding = fila.children[0]?.textContent.toLowerCase() || '';
        const colaborador = fila.children[1]?.textContent.toLowerCase() || '';
        const causa = fila.children[2]?.textContent.toLowerCase() || '';

        // Comprobamos si el texto ingresado coincide con alguna de las celdas
        const coincide = idOffboarding.includes(textoBusqueda) || 
                         colaborador.includes(textoBusqueda) || 
                         causa.includes(textoBusqueda);

        // Muestra u oculta la fila según la coincidencia
        fila.style.display = coincide ? '' : 'none';
      });
    });
});