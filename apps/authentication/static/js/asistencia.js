function calcularAsistencia() {
    let entradaVal = document.getElementById("hora_entrada").value;
    let salidaVal = document.getElementById("hora_salida").value;
    
    let inputExtras = document.getElementById("horas_extras");
    // Opcional: si tienes un campo para horas trabajadas netas
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

    // Si la hora de salida es menor a la de entrada (ej. cambio de día)
    if (minSalida < minEntrada) {
        if (inputExtras) inputExtras.value = "00:00:00";
        return;
    }

    // ------------------------------------------------------------------
    // 1. CÁLCULO DE HORAS TRABAJADAS NETAS (Se resta 1 hora de almuerzo)
    // ------------------------------------------------------------------
    let minutosTotales = minSalida - minEntrada;
    let MINUTOS_ALMUERZO = 60; // 1 hora de almuerzo descontada

    // Aplicar descuento de almuerzo solo si permaneció más de 1 hora
    let minutosEfectivos = minutosTotales > MINUTOS_ALMUERZO ? minutosTotales - MINUTOS_ALMUERZO : minutosTotales;

    let hTrabajadas = Math.floor(minutosEfectivos / 60);
    let mTrabajados = minutosEfectivos % 60;

    if (inputTrabajadas) {
        inputTrabajadas.value = 
            String(hTrabajadas).padStart(2, '0') + ":" + 
            String(mTrabajados).padStart(2, '0') + ":00";
    }

    // ------------------------------------------------------------------
    // 2. CÁLCULO DE HORAS EXTRAS (A partir de las 17:00 PM / 1020 min)
    // ------------------------------------------------------------------
    let MIN_HORA_SALIDA_OFICIAL = 17 * 60; // 17:00 PM en minutos (1020)
    let minExtras = 0;

    // Solo acumula extras si la hora de salida sobrepasa las 17:00
    if (minSalida > MIN_HORA_SALIDA_OFICIAL) {
        minExtras = minSalida - MIN_HORA_SALIDA_OFICIAL;
    }

    let hExtras = Math.floor(minExtras / 60);
    let mExtras = minExtras % 60;

    if (inputExtras) {
        inputExtras.value = 
            String(hExtras).padStart(2, '0') + ":" + 
            String(mExtras).padStart(2, '0') + ":00";
    }
}

// Asignar los eventos "change" e "input" para que calcule automáticamente
document.getElementById("hora_entrada").addEventListener("change", calcularAsistencia);
document.getElementById("hora_salida").addEventListener("change", calcularAsistencia);
document.getElementById("hora_entrada").addEventListener("input", calcularAsistencia);
document.getElementById("hora_salida").addEventListener("input", calcularAsistencia);