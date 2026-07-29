document.addEventListener("DOMContentLoaded", function () {
        const idKPIInput = document.getElementById("id_KPI");
        const sectionDetalle = document.getElementById("section-detalle");

        // Si Django ya generó y retornó un ID de cabecera válido
        if (idKPIInput && idKPIInput.value !== "") {
          if (sectionDetalle) {
            // Desbloquear visualmente y habilitar la sección de detalles
            sectionDetalle.classList.remove("section-disabled");
            sectionDetalle.style.opacity = "1";
            sectionDetalle.style.pointerEvents = "auto";

            const inputsDetalle = sectionDetalle.querySelectorAll(
              "select, input, button",
            );
            inputsDetalle.forEach((elemento) => {
              elemento.removeAttribute("disabled");
            });
          }
        }
});

document.addEventListener("DOMContentLoaded", function () {
  // 1. Obtener la referencia al input que contiene el ID de cabecera y a la sección de detalle
  const inputCabeceraId = document.getElementById("id_KPI");
  const sectionDetalle = document.getElementById("section-detalle");
  const formDetalle = document.getElementById("form-detalle");

  // 2. Verificar si existe un ID de cabecera válido
  const cabeceraExiste = inputCabeceraId && inputCabeceraId.value.trim() !== "";

  if (!cabeceraExiste) {
    // OPCIÓN A: Ocultar completamente la sección si no hay cabecera
    if (formDetalle) {
      formDetalle.style.display = "none";
    }

    /* 
    // OPCIÓN B: Si prefieres mostrar la sección pero completamente deshabilitada visualmente,
    // descomenta las siguientes líneas y comenta la OPCIÓN A de arriba:
    
    if (sectionDetalle) {
      sectionDetalle.style.opacity = "0.4";
      sectionDetalle.style.pointerEvents = "none";
    }
    if (formDetalle) {
      const inputsDetalle = formDetalle.querySelectorAll("input, select, button");
      inputsDetalle.forEach(element => element.disabled = true);
    }
    */
  } else {
    // Si la cabecera ya existe (Django rellenó kpi_cabecera_id)
    if (formDetalle) {
      formDetalle.style.display = "block";
    }
    if (sectionDetalle) {
      sectionDetalle.style.opacity = "1";
      sectionDetalle.style.pointerEvents = "auto";
    }
  }
});