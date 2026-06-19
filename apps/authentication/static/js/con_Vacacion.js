const empleado = document.getElementById("empleado");

empleado.addEventListener("change", function(){

    fetch(
        `/obtener_saldo_vacaciones/?empleado=${this.value}`
    )

    .then(response => response.json())

    .then(data => {

        document.getElementById("dias_acumulados").value =
            data.acumulados;

        document.getElementById("dias_tomados").value =
            data.tomados;

        document.getElementById("dias_disponibles").value =
            data.disponibles;

    });

});