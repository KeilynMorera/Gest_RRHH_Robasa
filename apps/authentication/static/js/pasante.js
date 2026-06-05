document.addEventListener('DOMContentLoaded', function () {
    // Seleccionamos el input de búsqueda por su ID
    const inputFiltro = document.getElementById('filtro-tabla');
    // Seleccionamos todas las filas de datos dentro del cuerpo de la tabla
    const filasTabla = document.querySelectorAll('#tabla-pasantes tbody tr');

    // Escuchamos el evento 'input' para capturar la búsqueda en tiempo real
    inputFiltro.addEventListener('input', function () {
        // Convertimos el término de búsqueda a minúsculas para que no importe si es MAYÚSCULA o minúscula
        const terminoBusqueda = this.value.toLowerCase().trim();

        filasTabla.forEach(fila => {
            // Saltamos la fila de "No existen pasantes" si está visible
            if (fila.querySelector('.tabla-vacia')) return;

            // Obtenemos todo el texto de la fila actual y lo pasamos a minúsculas
            const textoFila = fila.textContent.toLowerCase();

            // Si el texto de la fila incluye lo que el usuario escribió, la mostramos. Si no, la ocultamos.
            if (textoFila.includes(terminoBusqueda)) {
                fila.style.display = ''; // Restablece el display original (table-row)
            } else {
                fila.style.display = 'none'; // Oculta la fila
            }
        });
    });
});