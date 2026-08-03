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

document.addEventListener("DOMContentLoaded", function () {
  const selectEmpleado = document.getElementById("idEmpleado");

  // Elementos Salario
  const inputSalarioActual = document.getElementById("salario_actual");
  const contenedorSalario = document.getElementById("contenedor-salario-actual");
  const inputIdSalario = document.getElementById("idSalarioEmpleado");

  // Elementos Premio Actual
  const inputPremioActual = document.getElementById("premio_actual");
  const contenedorPremio = document.getElementById("contenedor-premio-actual");
  const inputIdPremio = document.getElementById("idPremioAsignado");

  // Elementos Nuevo Premio
  const inputNuevoPremio = document.getElementById("nuevo_premio");
  const contenedorNuevoPremio = document.getElementById("contenedor-nuevo-premio");

  // ==========================================================
  // 1. APLICAR BLOQUEO VISUAL Y DE EDICIÓN
  // ==========================================================
  function bloquearCampoLectura(inputElement) {
    if (!inputElement) return;

    // A. Atributo HTML y estilo visual de casilla bloqueada
    inputElement.setAttribute("readonly", true);
    inputElement.tabIndex = -1; // Evita que gane foco con la tecla TAB
    inputElement.style.backgroundColor = "#e9ecef";
    inputElement.style.cursor = "not-allowed";

    // B. Bloqueo de entrada por teclado o pegado
    inputElement.addEventListener("keydown", function (e) {
      e.preventDefault();
      return false;
    });

    inputElement.addEventListener("paste", function (e) {
      e.preventDefault();
      return false;
    });
  }

  // Aplicamos el bloqueo a las casillas "Actuales"
  bloquearCampoLectura(inputSalarioActual);
  bloquearCampoLectura(inputPremioActual);

  // ==========================================================
  // 2. CÓDIGO FETCH / AJAX
  // ==========================================================
  if (selectEmpleado) {
    selectEmpleado.addEventListener("change", function () {
      const idEmpleado = this.value;

      // Reseteo si se deselecciona el empleado
      if (!idEmpleado) {
        if (inputSalarioActual) inputSalarioActual.value = "";
        if (inputPremioActual) inputPremioActual.value = "";
        if (inputNuevoPremio) inputNuevoPremio.value = "";

        if (contenedorSalario) contenedorSalario.style.display = "none";
        if (contenedorPremio) contenedorPremio.style.display = "none";
        if (contenedorNuevoPremio) contenedorNuevoPremio.style.display = "none";
        return;
      }

      // Consulta al backend Django
      fetch(`/api/obtener-salario-empleado/${idEmpleado}/`)
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            // --- 1. CARGA SALARIO ACTUAL ---
            if (inputSalarioActual) {
              const montoSalario = parseFloat(data.salario_neto) || 0;
              inputSalarioActual.value = `₡${montoSalario.toLocaleString("es-CR", { minimumFractionDigits: 2 })}`;
            }
            if (inputIdSalario) inputIdSalario.value = data.idSalario || "";
            if (contenedorSalario) contenedorSalario.style.display = "block";

            // --- 2. CARGA PREMIO ACTUAL ---
            if (inputPremioActual) {
              // Revisa si viene como 'premio_actual', 'premio' o 'monto_premio'
              const valorRaw = data.premio_actual ?? data.premio ?? data.monto_premio ?? 0;
              const montoPremio = parseFloat(valorRaw) || 0;

              inputPremioActual.value = `₡${montoPremio.toLocaleString("es-CR", { minimumFractionDigits: 2 })}`;
            }
            if (inputIdPremio) inputIdPremio.value = data.idPremio || data.idPremioAsignado || "";
            if (contenedorPremio) contenedorPremio.style.display = "block";

            // --- 3. MOSTRAR CAMPO PARA NUEVO PREMIO ---
            if (contenedorNuevoPremio) {
              contenedorNuevoPremio.style.display = "block";
              if (inputNuevoPremio) inputNuevoPremio.value = "";
            }

          } else {
            if (inputSalarioActual) inputSalarioActual.value = "Sin registro";
            if (inputPremioActual) inputPremioActual.value = "Sin registro";
            if (contenedorNuevoPremio) contenedorNuevoPremio.style.display = "none";
          }
        })
        .catch((error) => {
          console.error("Error al cargar la información:", error);
          if (inputSalarioActual) inputSalarioActual.value = "Error al cargar";
          if (inputPremioActual) inputPremioActual.value = "Error al cargar";
          if (contenedorNuevoPremio) contenedorNuevoPremio.style.display = "none";
        });
    });
  }
});