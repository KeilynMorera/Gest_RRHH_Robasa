document.addEventListener("DOMContentLoaded", function () {
        const selCuadrante = document.getElementById("idCuadrante_9box");
        const selPerfil = document.getElementById("idCuadrante_9box_Perfil");
        const selDesempeno = document.getElementById(
          "idCuadrante_9box_Desempeno",
        );
        const selPotencial = document.getElementById(
          "idCuadrante_9box_Potencial",
        );
        const txtPlan = document.getElementById("Plan_Accion");

        const prevCodigo = document.getElementById("preview-codigo");
        const prevPerfil = document.getElementById("preview-perfil");
        const prevPlan = document.getElementById("preview-plan");
        const prevDesempeno = document.getElementById("preview-desempeno");
        const prevPotencial = document.getElementById("preview-potencial");

        const miniBoxes = document.querySelectorAll(".mini-box");

        function actualizarPreview() {
          // 🔹 Texto del cuadrante (M1, M2, etc.)
          const codigoTexto =
            selCuadrante.options[selCuadrante.selectedIndex]?.text || "—";

          // 🔹 VALUE (ID) para comparar en la matriz
          const codigoValue = selCuadrante.value;

          prevCodigo.textContent = codigoTexto;

          // Perfil
          prevPerfil.textContent =
            selPerfil.options[selPerfil.selectedIndex]?.text ||
            "Seleccione un perfil";

          // Desempeño
          prevDesempeno.textContent =
            selDesempeno.options[selDesempeno.selectedIndex]?.text || "—";

          // Potencial
          prevPotencial.textContent =
            selPotencial.options[selPotencial.selectedIndex]?.text || "—";

          // Plan
          prevPlan.textContent =
            txtPlan.value || "El plan de acción aparecerá aquí...";

          // 🔥 Resaltar cuadrante correcto
          miniBoxes.forEach((box) => {
            box.classList.toggle("active", box.dataset.codigo === codigoTexto);
          });
        }

        // Eventos
        selCuadrante.addEventListener("change", actualizarPreview);
        selPerfil.addEventListener("change", actualizarPreview);
        selDesempeno.addEventListener("change", actualizarPreview);
        selPotencial.addEventListener("change", actualizarPreview);
        txtPlan.addEventListener("input", actualizarPreview);
});