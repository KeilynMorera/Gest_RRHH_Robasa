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