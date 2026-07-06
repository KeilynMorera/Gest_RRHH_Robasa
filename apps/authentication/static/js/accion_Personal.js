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



    //==============================
    // OCULTAR TODO
    //==============================

    function ocultarCampos(){

        contSalarioActual.style.display = "none";
        contNuevoSalario.style.display = "none";

        contPremioActual.style.display = "none";
        contNuevoPremio.style.display = "none";

        salarioActual.value = "";
        premioActual.value = "";

        idSalarioEmpleado.value = "";
        idPremioAsignado.value = "";
    }



    //==============================
    // OBTENER SALARIO
    //==============================

    function cargarSalario(idEmpleado){

        fetch(`/accion/obtener-salario/?idEmpleado=${idEmpleado}`)

        .then(response => response.json())

        .then(data=>{

            if(data.success){

                salarioActual.value =
                    Number(data.salario).toLocaleString(
                        "es-CR",
                        {
                            minimumFractionDigits:2,
                            maximumFractionDigits:2
                        }
                    );

                idSalarioEmpleado.value =
                    data.idSalarioEmpleado;

            }else{

                salarioActual.value = "";
                idSalarioEmpleado.value = "";

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

                premioActual.value =
                Number(data.monto).toLocaleString(
                    "es-CR",
                    {
                        minimumFractionDigits:2,
                        maximumFractionDigits:2
                    }
                );

                idPremioAsignado.value = data.idPremioAsignado;

                // ESTE ES EL QUE SE ENVIARÁ AL BACKEND
                document.getElementById("monto_premio").value = data.monto;

            }else{

                premioActual.value="";
                idPremioAsignado.value="";

                alert(data.mensaje);

            }

        });

    }



    //==============================
    // CAMBIO DE TIPO DE ACCIÓN
    //==============================

    tipoAccion.addEventListener("change", function(){

        ocultarCampos();

        if(!empleado.value){
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

            contSalarioActual.style.display="block";
            contNuevoSalario.style.display="block";

            cargarSalario(
                empleado.value
            );

        }



        //--------------------------
        // PREMIO
        //--------------------------

        else if(nombre==="Premio"){

            contPremioActual.style.display="block";
            contNuevoPremio.style.display="block";

            cargarPremio(
                empleado.value
            );

        }

    });



    //==============================
    // SI CAMBIAN EL EMPLEADO
    //==============================

    empleado.addEventListener("change",function(){

        ocultarCampos();

        tipoAccion.selectedIndex=0;

    });

});
