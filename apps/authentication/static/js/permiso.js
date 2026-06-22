document.addEventListener("DOMContentLoaded", function () {

    const filtro = document.getElementById("filtro-permiso");
    const tabla = document.getElementById("tabla-permisos");
    const filas = tabla.getElementsByTagName("tbody")[0].getElementsByTagName("tr");

    filtro.addEventListener("keyup", function () {

        let texto = filtro.value.toLowerCase();

        for (let i = 0; i < filas.length; i++) {

            let nombreEmpleado = filas[i].cells[1].textContent.toLowerCase();
            let fecha = filas[i].cells[2].textContent.toLowerCase();

            if (
                nombreEmpleado.includes(texto) ||
                fecha.includes(texto)
            ) {
                filas[i].style.display = "";
            }
            else {
                filas[i].style.display = "none";
            }
        }
    });

});