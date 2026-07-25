function calcularAsistencia() {
    let entradaVal = document.getElementById("hora_entrada").value;
    let salidaVal = document.getElementById("hora_salida").value;
    
    let inputExtras = document.getElementById("horas_extras");
    let inputTrabajadas = document.getElementById("horas_trabajadas"); 

    if (!entradaVal || !salidaVal) {
        if (inputExtras) inputExtras.value = "00:00:00";
        if (inputTrabajadas) inputTrabajadas.value = "00:00:00";
        return;
    }

    // Convertir horas "HH:MM" a minutos desde las 00:00
    let [hE, mE] = entradaVal.split(':').map(Number);
    let [hS, mS] = salidaVal.split(':').map(Number);

    let minEntrada = hE * 60 + mE;
    let minSalida = hS * 60 + mS;

    // Si la hora de salida es menor a la de entrada
    if (minSalida < minEntrada) {
        if (inputExtras) inputExtras.value = "00:00:00";
        if (inputTrabajadas) inputTrabajadas.value = "00:00:00";
        return;
    }

    // ------------------------------------------------------------------
    // 1. CÁLCULO DE HORAS TRABAJADAS NETAS (Resta 1 hora de almuerzo)
    // ------------------------------------------------------------------
    let minutosTotalesReloj = minSalida - minEntrada;
    let MINUTOS_ALMUERZO = 60; // 1 hora de almuerzo

    // Descuenta almuerzo solo si estuvo en las instalaciones más de 1 hora
    let minutosEfectivos = minutosTotalesReloj > MINUTOS_ALMUERZO 
        ? minutosTotalesReloj - MINUTOS_ALMUERZO 
        : minutosTotalesReloj;

    let hTrabajadas = Math.floor(minutosEfectivos / 60);
    let mTrabajados = minutosEfectivos % 60;

    if (inputTrabajadas) {
        inputTrabajadas.value = 
            String(hTrabajadas).padStart(2, '0') + ":" + 
            String(mTrabajados).padStart(2, '0') + ":00";
    }

    // ------------------------------------------------------------------
    // 2. CÁLCULO DE HORAS EXTRAS
    // Jornada ordinaria: 07:00 a 17:00 (10 hrs reloj - 1 hr almuerzo = 9 hrs efectivas / 540 min)
    // Hora oficial de salida: 17:00 (1020 min)
    // ------------------------------------------------------------------
    let HORA_SALIDA_OFICIAL_MIN = 17 * 60; // 1020 minutos (5:00 PM)
    let minExtras = 0;

    // Calcula horas extras solo si se retira después de las 17:00 PM
    if (minSalida > HORA_SALIDA_OFICIAL_MIN) {
        minExtras = minSalida - HORA_SALIDA_OFICIAL_MIN;
    }

    let hExtras = Math.floor(minExtras / 60);
    let mExtras = minExtras % 60;

    if (inputExtras) {
        inputExtras.value = 
            String(hExtras).padStart(2, '0') + ":" + 
            String(mExtras).padStart(2, '0') + ":00";
    }
}

// Asignar los eventos
document.getElementById("hora_entrada").addEventListener("change", calcularAsistencia);
document.getElementById("hora_salida").addEventListener("change", calcularAsistencia);
document.getElementById("hora_entrada").addEventListener("input", calcularAsistencia);
document.getElementById("hora_salida").addEventListener("input", calcularAsistencia);


document.addEventListener('DOMContentLoaded', () => {
    // 1. Obtener referencias al input de búsqueda y a las filas de la tabla
    const inputFiltro = document.getElementById('filtro-asistencia');
    const tabla = document.getElementById('tabla-asistencia');
    
    if (!inputFiltro || !tabla) return; // Validación de existencia
    
    const filas = tabla.querySelectorAll('tbody tr');

    // 2. Escuchar el evento de escritura en el input
    inputFiltro.addEventListener('keyup', () => {
        const busqueda = inputFiltro.value.toLowerCase().trim();

        filas.forEach(fila => {
            // Ignorar la fila que muestra el mensaje "No existen registros..." si está vacía
            if (fila.querySelector('.tabla-vacia')) return;

            // Obtener la columna del empleado (segunda columna: índice 1)
            const colEmpleado = fila.cells[1];

            if (colEmpleado) {
                const nombreEmpleado = colEmpleado.textContent.toLowerCase();
                
                // Mostrar u ocultar la fila según coincida la búsqueda
                if (nombreEmpleado.includes(busqueda)) {
                    fila.style.display = '';
                } else {
                    fila.style.display = 'none';
                }
            }
        });
    });
});