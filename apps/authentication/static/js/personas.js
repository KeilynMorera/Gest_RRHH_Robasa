document.addEventListener("DOMContentLoaded", function () {
    const filtro = document.getElementById("filtro-tabla");
    const filas = document.querySelectorAll("#tabla-personas tbody tr");

    filtro.addEventListener("keyup", function () {
      const texto = this.value.toLowerCase().trim();

      filas.forEach(function (fila) {
        // Ignora la fila del mensaje "No hay personas registradas"
        if (fila.querySelector(".tabla-vacia")) {
          return;
        }

        const nombre = fila.children[1].textContent.toLowerCase();
        const cedula = fila.children[2].textContent.toLowerCase();

        if (nombre.includes(texto) || cedula.includes(texto)) {
          fila.style.display = "";
        } else {
          fila.style.display = "none";
        }
      });
    });
});

const fotoInput = document.getElementById("foto");
const preview = document.getElementById("foto-preview");

if (fotoInput) {

    fotoInput.addEventListener("change", function () {

        const archivo = this.files[0];

        if (archivo) {

            const lector = new FileReader();

            lector.onload = function (e) {

                preview.src = e.target.result;

            };

            lector.readAsDataURL(archivo);

        }

    });

}