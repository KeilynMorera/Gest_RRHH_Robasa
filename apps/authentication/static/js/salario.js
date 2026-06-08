document
.getElementById("filtro-salarios")
.addEventListener("keyup", function () {

    let filtro = this.value.toLowerCase();

    let filas = document.querySelectorAll(
        "#tabla-salarios tbody tr"
    );

    filas.forEach(function (fila) {

        let texto = fila.textContent.toLowerCase();

        fila.style.display =
            texto.includes(filtro)
            ? ""
            : "none";
    });

});




document.addEventListener("DOMContentLoaded", function () {

    const empleadoSelect = document.getElementById("empleado");

    empleadoSelect.addEventListener("change", function () {

        const empleadoId = this.value;

        if (!empleadoId) return;

        fetch(`/obtener-compensacion-empleado/${empleadoId}/`)
        .then(response => response.json())
        .then(data => {

            if (data.success) {

                document.getElementById("salario_bruto").value =
                    data.salario_bruto;

                document.getElementById("salario_sem_neto").value =
                    data.salario_sem_neto;

                document.getElementById("comision_base").value =
                    data.comision_base;

                document.getElementById("variable_base").value =
                    data.variable_base;

                document.getElementById("viaticos_alimenticios").value =
                    data.viaticos_alimenticios;

                document.getElementById("kilometraje_base").value =
                    data.kilometraje_base;

                document.getElementById("bono_base").value =
                    data.bono_base;

            } else {

                alert(data.mensaje);

            }

        })
        .catch(error => {

            console.error(error);

        });

    });

});