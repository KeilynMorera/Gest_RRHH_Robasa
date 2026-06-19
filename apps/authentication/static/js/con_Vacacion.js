document.getElementById("empleado").addEventListener("change", function(){

    let empleadoId = this.value;

    if(empleadoId==""){
        return;
    }

    fetch(`/obtener_saldo_vacaciones/${empleadoId}/`)

    .then(response => response.json())

    .then(data => {

        document.getElementById("dias_acumulados").value =
            data.dias_acumulados;

        document.getElementById("dias_tomados").value =
            data.dias_tomados;

        document.getElementById("dias_disponibles").value =
            data.dias_disponibles;

    });

});