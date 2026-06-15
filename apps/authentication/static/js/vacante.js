document.getElementById('puesto').addEventListener('change', function() {

    const puestoId = this.value;

    fetch(`/obtener-compensacion-puesto/${puestoId}/`)
    .then(response => {

        console.log("STATUS:", response.status);

        return response.json();

    })
    .then(data => {

        console.log(data);

        if (data.success) {

            // ==============================
            // CAMPOS VISIBLES
            // ==============================

            document.getElementById("salario_bruto").value =
                data.salario_bruto;

            document.getElementById("compensacion_total").value =
                data.compensacion_total;

            // ==============================
            // CAMPOS OCULTOS PARA GUARDAR
            // ==============================

            document.getElementById("salario_bruto_hidden").value =
                data.salario_bruto;

            document.getElementById("compensacion_total_hidden").value =
                data.compensacion_total;

        } else {

            document.getElementById("salario_bruto").value = '';

            document.getElementById("compensacion_total").value = '';

            document.getElementById("salario_bruto_hidden").value = '';

            document.getElementById("compensacion_total_hidden").value = '';

            console.log(data.mensaje);
        }

    })
    .catch(error => {

        console.error(error);

    });

    console.log("Puesto seleccionado:", this.value);

});


document.addEventListener("DOMContentLoaded", function () {

    const filtro = document.getElementById("filtro-tabla");
    const tabla = document.getElementById("tabla-vacantes");
    const filas = tabla.getElementsByTagName("tbody")[0].getElementsByTagName("tr");

    filtro.addEventListener("keyup", function () {

        let textoBusqueda = filtro.value.toLowerCase();

        for (let i = 0; i < filas.length; i++) {

            let titulo = filas[i].cells[1].textContent.toLowerCase();
            let puesto = filas[i].cells[2].textContent.toLowerCase();

            if (
                titulo.includes(textoBusqueda) ||
                puesto.includes(textoBusqueda)
            ) {
                filas[i].style.display = "";
            } else {
                filas[i].style.display = "none";
            }
        }
    });

});
