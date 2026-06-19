function calcularHorasExtra(){

    let entrada = document.getElementById("hora_entrada").value;

    let salida = document.getElementById("hora_salida").value;

    let extras = document.getElementById("horas_extras");


    if(!entrada || !salida){

        extras.value = "00:00:00";

        return;
    }


    let e = new Date("1970-01-01T"+entrada);

    let s = new Date("1970-01-01T"+salida);


    let horasTrabajadas = (s - e)/(1000*60*60);


    let extra = horasTrabajadas - 8;


    if(extra <= 0){

        extras.value = "00:00:00";

        return;
    }


    let horas = Math.floor(extra);

    let minutos = Math.round((extra-horas)*60);


    extras.value =

        String(horas).padStart(2,'0')

        + ":"

        + String(minutos).padStart(2,'0')

        + ":00";

}


document.getElementById("hora_entrada")

.addEventListener("change",calcularHorasExtra);


document.getElementById("hora_salida")

.addEventListener("change",calcularHorasExtra);




document.addEventListener("DOMContentLoaded", function () {

  const filtro = document.getElementById("filtro-asistencia");
  const filas  = document.querySelectorAll("#tabla-asistencia tbody tr");

  if (!filtro) return;

  filtro.addEventListener("keyup", function () {
    const texto = this.value.toLowerCase().trim();

    filas.forEach(function (fila) {

      // Ignora la fila vacía
      if (fila.querySelector(".tabla-vacia")) return;

      // [1] Nombre del empleado  [2] Fecha
      const nombre = fila.children[1]?.textContent.toLowerCase() ?? "";
      const fecha  = fila.children[2]?.textContent.toLowerCase() ?? "";

      const coincide = nombre.includes(texto) || fecha.includes(texto);

      fila.style.display = coincide ? "" : "none";
    });

    // Mensaje dinámico si no hay resultados
    const mensajeDinamico = document.getElementById("sin-resultados-asistencia");
    if (mensajeDinamico) mensajeDinamico.remove();

    const visibles = [...filas].filter(f =>
      !f.querySelector(".tabla-vacia") && f.style.display !== "none"
    );

    if (visibles.length === 0 && texto !== "") {
      const tbody = document.querySelector("#tabla-asistencia tbody");
      const fila  = document.createElement("tr");
      fila.id     = "sin-resultados-asistencia";
      fila.innerHTML = `
        <td colspan="8" class="tabla-vacia">
          <i class="fas fa-magnifying-glass"></i>
          No se encontraron registros para "<strong>${texto}</strong>"
        </td>`;
      tbody.appendChild(fila);
    }
  });

});