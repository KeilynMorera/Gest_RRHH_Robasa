document.addEventListener("DOMContentLoaded", function () {
    // ==============================
    // ELEMENTOS PRINCIPALES
    // ==============================
    const formCabecera = document.getElementById("form-cabecera");

    const selectorAccion = document.getElementById("Tipo_Accion");
    const selectorEmpleado = document.getElementById("idEmpleado");

    const contPremio = document.getElementById("contenedor-monto-premio");
    const inputPremio = document.getElementById("monto_premio");

    const contSalActual = document.getElementById(
        "contenedor-salario-actual",
    );
    const contNuevSal = document.getElementById("contenedor-nuevo-salario");

    const inputSalActual = document.getElementById("salario_actual");
    const inputNuevSal = document.getElementById("nuevo_salario");

    const colSelect = document.getElementById("columna-tipo-accion");
    const labelNuevoSalario = document.querySelector(
        "label[for='nuevo_salario']",
    );

    // ==============================
    // FUNCIONES AUXILIARES
    // ==============================

    function actualizarSalarioActual() {
        const opcion =
            selectorEmpleado.options[selectorEmpleado.selectedIndex];
        const salario = opcion?.dataset.salario || "0";

        inputSalActual.value =
            "₡" +
            parseFloat(salario).toLocaleString("es-CR", {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2,
            });
        }

    function resetCampos() {
        contPremio.style.display = "none";
        contSalActual.style.display = "none";
        contNuevSal.style.display = "none";

        inputPremio.required = false;
        inputPremio.value = "";

        inputNuevSal.required = false;
        inputNuevSal.value = "";
    }

    // ==============================
    // VALIDACIÓN FORM CABECERA
    // ==============================
    formCabecera.addEventListener("submit", function (e) {
        const empleadoInput = document.querySelector("[name='idEmpleado']");
        const fechaInput = document.querySelector("[name='Fecha']");
        
        if (!empleadoInput.value || !fechaInput.value) {
            e.preventDefault();
            alert("Debe seleccionar colaborador y fecha.");
        }
    });

    // ==============================
    // CAMBIO DE EMPLEADO
    // ==============================
    selectorEmpleado.addEventListener("change", function () {
        actualizarSalarioActual();
    });

    // ==============================
    // CAMBIO DE TIPO DE ACCIÓN
    // ==============================
    selectorAccion.addEventListener("change", function () {
        const opcion = this.options[this.selectedIndex];
        const nombreAccion = opcion?.getAttribute("data-name");

        resetCampos();

        colSelect.style.gridColumn = "span 2";

        if (nombreAccion === "Premio") {
            colSelect.style.gridColumn = "span 1";
            contPremio.style.display = "block";
            inputPremio.required = true;
        } else if (
            nombreAccion === "Ajuste Salarial" ||
            nombreAccion === "Ascenso"
        ) {
            contSalActual.style.display = "block";
            contNuevSal.style.display = "block";
            inputNuevSal.required = true;

            actualizarSalarioActual();
            
            if (nombreAccion === "Ascenso") {
                labelNuevoSalario.innerHTML =
                    '<i class="fas fa-arrow-up-right-dots field-icon"></i> Nuevo Salario por Ascenso <span class="req">*</span>';
                inputNuevSal.placeholder = "Ej: 550000";
            } else {
                labelNuevoSalario.innerHTML =
                    '<i class="fas fa-coins field-icon"></i> Nuevo Salario Bruto Propuesto <span class="req">*</span>';
                inputNuevSal.placeholder = "Ej: 450000";
            }
        }
    });

    // ==============================
    // RESET LIMPIAR
    // ==============================
    document
    .getElementById("btn-limpiar")
    .addEventListener("click", function () {
        setTimeout(() => {
            selectorAccion.dispatchEvent(new Event("change"));
        }, 10);
    });
});



document.addEventListener("DOMContentLoaded", function () {

  const input = document.getElementById("filtro-acciones");
  const tabla = document.getElementById("tabla-acciones");
  const filas = tabla.getElementsByTagName("tbody")[0].getElementsByTagName("tr");

  input.addEventListener("keyup", function () {

    const filtro = this.value.toLowerCase().trim();

    for (let i = 0; i < filas.length; i++) {

      const celdas = filas[i].getElementsByTagName("td");

      if (celdas.length === 0) continue; // por el empty row

      const empleado = celdas[1].textContent.toLowerCase(); // Columna Empleado
      const fecha = celdas[5].textContent.toLowerCase();     // Columna Fecha
      const accion = celdas[2].textContent.toLowerCase();    // opcional

      if (
        empleado.includes(filtro) ||
        fecha.includes(filtro) ||
        accion.includes(filtro)
      ) {
        filas[i].style.display = "";
      } else {
        filas[i].style.display = "none";
      }
    }

  });

});


fetch(`/obtener-premio/${idEmpleado}/`)
.then(r=>r.json())
.then(data=>{

    if(data.success){

        document.getElementById("premio_actual").value =
            "₡" + Number(data.premio).toLocaleString();

        document.getElementById("idPremio").value =
            data.idPremio;

    }

});