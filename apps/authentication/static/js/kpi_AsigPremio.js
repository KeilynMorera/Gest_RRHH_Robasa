document.addEventListener("DOMContentLoaded", function () {
        // =====================================================
        // ELEMENTOS
        // =====================================================

        const premioSelect = document.getElementById("idPremio");

        const kpiSelect = document.getElementById("id_KPI");

        const montoLiquidadoPreview = document.getElementById(
          "Monto_Liquidado_Preview",
        );

        const btnLimpiar = document.getElementById("btn-limpiar");

        // =====================================================
        // VALIDAR ELEMENTOS
        // =====================================================

        if (!premioSelect || !kpiSelect || !montoLiquidadoPreview) {
          console.error(
            "No se encontraron los elementos necesarios para calcular el monto liquidado.",
          );

          return;
        }

        // =====================================================
        // FORMATEAR MONTO
        // =====================================================

        function formatearMonto(monto) {
          return new Intl.NumberFormat("es-CR", {
            style: "currency",
            currency: "CRC",
            minimumFractionDigits: 2,
            maximumFractionDigits: 2,
          }).format(monto);
        }

        // =====================================================
        // LIMPIAR MONTO
        // =====================================================

        function limpiarMonto() {
          montoLiquidadoPreview.value = "₡ 0,00";
        }

        // =====================================================
        // OBTENER MONTO LIQUIDADO
        //
        // Se consulta:
        //
        // Premio seleccionado
        // +
        // KPI seleccionado
        //
        // El servidor busca:
        //
        // Premio.Monto
        // +
        // KPI_Detalle.Monto_Total
        //
        // =====================================================

        function obtenerMontoLiquidado() {
          const idPremio = premioSelect.value;

          const idKPI = kpiSelect.value;

          // ===================================================
          // VALIDAR SELECCIONES
          // ===================================================

          if (!idPremio || !idKPI) {
            limpiarMonto();

            return;
          }

          // ===================================================
          // MOSTRAR CARGANDO
          // ===================================================

          montoLiquidadoPreview.value = "Calculando...";

          // ===================================================
          // URL DINÁMICA
          // ===================================================

          const url = `/premios-asignados/monto/${idPremio}/${idKPI}/`;

          // ===================================================
          // CONSULTAR SERVIDOR
          // ===================================================

          fetch(url)
            .then((response) => response.json())

            .then((data) => {
              // =============================================
              // RESPUESTA EXITOSA
              // =============================================

              if (data.success) {
                const monto = parseFloat(data.monto_liquidado);

                if (!isNaN(monto)) {
                  montoLiquidadoPreview.value = formatearMonto(monto);
                } else {
                  limpiarMonto();
                }
              }

              // =============================================
              // ERROR
              // =============================================
              else {
                limpiarMonto();

                console.error(
                  data.error || "No se pudo calcular el monto liquidado.",
                );
              }
            })

            .catch((error) => {
              console.error("Error al obtener el monto liquidado:", error);

              limpiarMonto();
            });
        }

        // =====================================================
        // EVENTO: CAMBIO DE PREMIO
        // =====================================================

        premioSelect.addEventListener("change", obtenerMontoLiquidado);

        // =====================================================
        // EVENTO: CAMBIO DE KPI
        // =====================================================

        kpiSelect.addEventListener("change", obtenerMontoLiquidado);

        // =====================================================
        // LIMPIAR CAMPOS
        // =====================================================

        if (btnLimpiar) {
          btnLimpiar.addEventListener("click", function () {
            setTimeout(function () {
              limpiarMonto();
            }, 50);
          });
        }
      });