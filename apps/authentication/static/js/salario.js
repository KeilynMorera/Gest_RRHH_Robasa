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

    console.log("salario.js cargado");

    const empleadoSelect = document.getElementById("empleado");

    console.log("Select encontrado:", empleadoSelect);

    if (!empleadoSelect) {
        console.error("No se encontró el select con id='empleado'");
        return;
    }

    empleadoSelect.addEventListener("change", function () {

        const empleadoId = this.value;

        console.log("Empleado seleccionado:", empleadoId);

        if (!empleadoId) {
            return;
        }

        fetch(`/obtener-compensacion-empleado/${empleadoId}/`)
            .then(response => response.json())
            .then(data => {

                console.log("Datos recibidos:", data);

                if (data.success) {

                    const salarioBruto =
                        document.getElementById("salario_bruto");

                    const salarioSemNeto =
                        document.getElementById("salario_sem_neto");

                    const comisionBase =
                        document.getElementById("comision_base");

                    const variableBase =
                        document.getElementById("variable_base");

                    const viaticos =
                        document.getElementById("viaticos_alimenticios");

                    const kilometraje =
                        document.getElementById("kilometraje_base");

                    const bono =
                        document.getElementById("bono_base");

                    console.log("Campos encontrados:", {
                        salarioBruto,
                        salarioSemNeto,
                        comisionBase,
                        variableBase,
                        viaticos,
                        kilometraje,
                        bono
                    });

                    if (salarioBruto)
                        salarioBruto.value = data.salario_bruto ?? 0;

                    if (salarioSemNeto)
                        salarioSemNeto.value = data.salario_sem_neto ?? 0;

                    if (comisionBase)
                        comisionBase.value = data.comision_base ?? 0;

                    if (variableBase)
                        variableBase.value = data.variable_base ?? 0;

                    if (viaticos)
                        viaticos.value = data.viaticos_alimenticios ?? 0;

                    if (kilometraje)
                        kilometraje.value = data.kilometraje_base ?? 0;

                    if (bono)
                        bono.value = data.bono_base ?? 0;

                } else {

                    console.error(data.mensaje);
                    alert(data.mensaje);

                }

            })
            .catch(error => {

                console.error("Error:", error);

            });

    });

});


function calcularCompensacionTotal() {

    const salario =
        parseFloat(document.getElementById("salario_bruto").value) || 0;

    const comision =
        parseFloat(document.getElementById("comision_base").value) || 0;

    const variable =
        parseFloat(document.getElementById("variable_base").value) || 0;

    const viaticos =
        parseFloat(document.getElementById("viaticos_alimenticios").value) || 0;

    const kilometraje =
        parseFloat(document.getElementById("kilometraje_base").value) || 0;

    const bono =
        parseFloat(document.getElementById("bono_base").value) || 0;

    const total =
        salario +
        comision +
        variable +
        viaticos +
        kilometraje +
        bono;

    document.getElementById("compensacion_total").value =
        total.toFixed(2);
}