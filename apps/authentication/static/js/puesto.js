/* ============================================================
BUSCADOR DE PUESTOS POR NOMBRE
============================================================ */

/*
Obtiene el campo de búsqueda del HTML.
En tu HTML corresponde a:

<input
 type="text"
 id="filtro-tabla"
 placeholder="Buscar puesto..."
/>
*/
const filtroTabla = document.getElementById("filtro-tabla");

/*
Obtiene la tabla donde se encuentran registrados los puestos.

En tu HTML corresponde a:

  <table class="data-table" id="tabla-puestos">
*/
const tablaPuestos = document.getElementById("tabla-puestos");

/* ============================================================
VERIFICAR QUE EXISTAN EL BUSCADOR Y LA TABLA
============================================================ */

if (filtroTabla && tablaPuestos) {

/*
Obtiene todas las filas (<tr>) que se encuentran
dentro del cuerpo de la tabla (<tbody>).
*/
const filas = tablaPuestos.querySelectorAll("tbody tr");

/* ==========================================================
EVENTO DE BÚSQUEDA
========================================================== */

/*
"input" se ejecuta cada vez que el usuario escribe
o elimina texto dentro del buscador.
*/
filtroTabla.addEventListener("input", function () {

/*
  Obtiene el texto escrito por el usuario.

  trim() elimina espacios al inicio y al final.

  toLowerCase() convierte todo a minúsculas para que
  la búsqueda no distinga entre mayúsculas y minúsculas.

  Ejemplos:

  "Gerente"  -> "gerente"
  "GERENTE"  -> "gerente"
  " gerente " -> "gerente"
*/
const textoBusqueda = filtroTabla.value
  .trim()
  .toLowerCase();


/* ========================================================
   RECORRER TODAS LAS FILAS DE LA TABLA
   ======================================================== */

filas.forEach(function (fila) {

  /*
    Obtiene las celdas (<td>) de la fila actual.
  */
  const celdas = fila.querySelectorAll("td");


  /*
    Verifica que la fila tenga al menos dos celdas.

    En tu tabla:

    td[0] = ID
    td[1] = Nombre Puesto
    td[2] = Descripción
    td[3] = Departamento
    td[4] = Acción
  */
  if (celdas.length >= 2) {

    /*
      Obtiene únicamente el nombre del puesto.

      En tu HTML corresponde a:

      <td>
        <strong>{{ puesto.Nombre }}</strong>
      </td>

      Por eso utilizamos celdas[1].
    */
    const nombrePuesto = celdas[1].textContent
      .trim()
      .toLowerCase();


    /* ====================================================
       COMPARAR LA BÚSQUEDA CON EL NOMBRE DEL PUESTO
       ==================================================== */

    /*
      includes() verifica si el texto escrito por el usuario
      está contenido dentro del nombre del puesto.

      Ejemplo:

      Puesto registrado:
      "Gerente de Recursos Humanos"

      Búsqueda:
      "gerente"

      Resultado:
      true

      Búsqueda:
      "recursos"

      Resultado:
      true
    */
    if (nombrePuesto.includes(textoBusqueda)) {

      /*
        Si coincide, muestra la fila.
      */
      fila.style.display = "";

    } else {

      /*
        Si no coincide, oculta la fila.
      */
      fila.style.display = "none";
    }
  }
});

});
}
