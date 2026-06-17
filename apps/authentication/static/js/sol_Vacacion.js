document.addEventListener("DOMContentLoaded", function () {

    const filtro = document.getElementById("filtro-vacaciones");
    const tabla = document.getElementById("tabla-vacaciones");
    const filas = tabla.getElementsByTagName("tbody")[0].getElementsByTagName("tr");

    filtro.addEventListener("keyup", function () {

        let texto = filtro.value.toLowerCase().trim();

        for (let i = 0; i < filas.length; i++) {

            // Columna Empleado
            let empleado = filas[i].cells[1].textContent.toLowerCase();

            // Columna Fecha Solicitud
            let fecha = filas[i].cells[2].textContent.toLowerCase();

            if (
                empleado.includes(texto) ||
                fecha.includes(texto)
            ) {
                filas[i].style.display = "";
            } else {
                filas[i].style.display = "none";
            }
        }

    });

});