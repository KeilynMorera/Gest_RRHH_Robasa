document.addEventListener("DOMContentLoaded", function () {

    //==============================
    // ELEMENTOS
    //==============================

    const empleado = document.getElementById("idEmpleado");
    const tipoAccion = document.getElementById("Tipo_Accion");

    const contSalarioActual = document.getElementById("contenedor-salario-actual");
    const contNuevoSalario = document.getElementById("contenedor-nuevo-salario");

    const contPremioActual = document.getElementById("contenedor-premio-actual");
    const contNuevoPremio = document.getElementById("contenedor-nuevo-premio");

    const salarioActual = document.getElementById("salario_actual");
    const idSalarioEmpleado = document.getElementById("idSalarioEmpleado");

    const premioActual = document.getElementById("premio_actual");
    const idPremioAsignado = document.getElementById("idPremioAsignado");

    // Elementos para el control de la Sección 2 y sus botones
    const seccionDetalle = document.getElementById("seccion-detalle");
    const inputFolio = document.getElementById("idAccion");


    //==============================
    // MOSTRAR/OCULTAR SECCIÓN 2 Y BOTONES
    //==============================

    function evaluarPasoDos() {
        if (!seccionDetalle) return;

        // Si existe el Folio con valor cargado, se muestra todo el bloque (formulario + botones)
        const tieneFolio = inputFolio && inputFolio.value.trim() !== "";

        if (tieneFolio) {
            seccionDetalle.style.display = "block";
        } else {
            seccionDetalle.style.display = "none";
        }
    }

    // Ejecución inicial al cargar el DOM
    evaluarPasoDos();


    //==============================
    // OCULTAR CAMPOS DINÁMICOS
    //==============================

    function ocultarCampos(){

        if (contSalarioActual) contSalarioActual.style.display = "none";
        if (contNuevoSalario) contNuevoSalario.style.display = "none";

        if (contPremioActual) contPremioActual.style.display = "none";
        if (contNuevoPremio) contNuevoPremio.style.display = "none";

        if (salarioActual) salarioActual.value = "";
        if (premioActual) premioActual.value = "";

        if (idSalarioEmpleado) idSalarioEmpleado.value = "";
        if (idPremioAsignado) idPremioAsignado.value = "";
    }


    //==============================
    // OBTENER SALARIO
    //==============================

    function cargarSalario(idEmpleado){

        fetch(`/accion/obtener-salario/?idEmpleado=${idEmpleado}`)

        .then(response => response.json())

        .then(data=>{

            if(data.success){

                if (salarioActual) {
                    salarioActual.value =
                        Number(data.salario).toLocaleString(
                            "es-CR",
                            {
                                minimumFractionDigits:2,
                                maximumFractionDigits:2
                            }
                        );
                }

                if (idSalarioEmpleado) {
                    idSalarioEmpleado.value = data.idSalarioEmpleado;
                }

            }else{

                if (salarioActual) salarioActual.value = "";
                if (idSalarioEmpleado) idSalarioEmpleado.value = "";

                alert(data.mensaje);
            }

        });

    }


    //==============================
    // OBTENER PREMIO
    //==============================

    function cargarPremio(idEmpleado){

        fetch(`/accion/obtener-premio/?idEmpleado=${idEmpleado}`)

        .then(response=>response.json())

        .then(data=>{

            if(data.success){

                if (premioActual) {
                    premioActual.value =
                    Number(data.monto).toLocaleString(
                        "es-CR",
                        {
                            minimumFractionDigits:2,
                            maximumFractionDigits:2
                        }
                    );
                }

                if (idPremioAsignado) {
                    idPremioAsignado.value = data.idPremioAsignado;
                }

                const inputMontoPremio = document.getElementById("monto_premio");
                if (inputMontoPremio) {
                    inputMontoPremio.value = data.monto;
                }

            }else{

                if (premioActual) premioActual.value="";
                if (idPremioAsignado) idPremioAsignado.value="";

                alert(data.mensaje);

            }

        });

    }


    //==============================
    // CAMBIO DE TIPO DE ACCIÓN
    //==============================

    if (tipoAccion) {
        tipoAccion.addEventListener("change", function(){

            ocultarCampos();

            if(empleado && !empleado.value){
                alert("Seleccione primero un empleado.");
                this.selectedIndex = 0;
                return;
            }

            const nombre =
                this.options[this.selectedIndex]
                    .dataset.name;


            //--------------------------
            // ASCENSO O AJUSTE
            //--------------------------

            if(
                nombre==="Ascenso" ||
                nombre==="Ajuste Salarial"
            ){

                if (contSalarioActual) contSalarioActual.style.display="block";
                if (contNuevoSalario) contNuevoSalario.style.display="block";

                if (empleado) {
                    cargarSalario(empleado.value);
                }

            }


            //--------------------------
            // PREMIO
            //--------------------------

            else if(nombre==="Premio"){

                if (contPremioActual) contPremioActual.style.display="block";
                if (contNuevoPremio) contNuevoPremio.style.display="block";

                if (empleado) {
                    cargarPremio(empleado.value);
                }

            }

        });
    }


    //==============================
    // SI CAMBIAN EL EMPLEADO
    //==============================

    if (empleado) {
        empleado.addEventListener("change",function(){

            ocultarCampos();

            if (tipoAccion) {
                tipoAccion.selectedIndex=0;
            }

        });
    }

});