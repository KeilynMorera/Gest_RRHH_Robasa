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