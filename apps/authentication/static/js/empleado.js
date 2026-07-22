document.addEventListener('DOMContentLoaded', () => {
    // 1. Obtener los elementos del DOM
    const inputFiltro = document.getElementById('filtro-tabla');
    const tablaEmpleados = document.getElementById('tabla-empleados');
    
    // Validar que los elementos existan en la página
    if (!inputFiltro || !tablaEmpleados) return;

    // 2. Evento para detectar la escritura en el buscador
    inputFiltro.addEventListener('keyup', () => {
        const busqueda = inputFiltro.value.toLowerCase().trim();
        const filas = tablaEmpleados.querySelectorAll('tbody tr');

        filas.forEach(fila => {
            // Ignorar la fila con el mensaje "No existen empleados registrados"
            if (fila.querySelector('.tabla-vacia')) return;

            // Obtener celdas correspondientes a Nombre (columna 1) y Puesto (columna 2)
            const celdaNombre = fila.cells[1]?.textContent.toLowerCase() || '';
            const celdaPuesto = fila.cells[2]?.textContent.toLowerCase() || '';

            // Verificar si alguna celda coincide con la búsqueda
            if (celdaNombre.includes(busqueda) || celdaPuesto.includes(busqueda)) {
                fila.style.display = ''; // Muestra la fila
            } else {
                fila.style.display = 'none'; // Oculta la fila
            }
        });
    });
});