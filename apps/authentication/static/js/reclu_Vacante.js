document.addEventListener('DOMContentLoaded', function () {

    const faseSelect =
        document.getElementById('fase_actual');

    actualizarTimeline();

    faseSelect.addEventListener(
        'change',
        actualizarTimeline
    );

    function actualizarTimeline() {

        const fase =
            parseInt(faseSelect.value || 1);

        const steps = [
            document.getElementById('step1'),
            document.getElementById('step2'),
            document.getElementById('step3'),
            document.getElementById('step4'),
            document.getElementById('step5')
        ];

        const lines = [
            document.getElementById('line1'),
            document.getElementById('line2'),
            document.getElementById('line3'),
            document.getElementById('line4')
        ];

        steps.forEach(step => {

            step.classList.remove(
                'completed',
                'active',
                'hired',
                'rejected',
                'disabled'
            );

        });

        lines.forEach(line => {

            line.classList.remove(
                'active',
                'hired'
            );

        });

        // ==========================
        // FASE 1
        // ==========================
        if (fase === 1){

            steps[0].classList.add('active');

        }

        // ==========================
        // FASE 2
        // ==========================
        else if (fase === 2){

            steps[0].classList.add('completed');
            lines[0].classList.add('active');

            steps[1].classList.add('active');

        }

        // ==========================
        // FASE 3
        // ==========================
        else if (fase === 3){

            steps[0].classList.add('completed');
            steps[1].classList.add('completed');

            lines[0].classList.add('active');
            lines[1].classList.add('active');

            steps[2].classList.add('active');

        }

        // ==========================
        // CONTRATADO
        // ==========================
        else if (fase === 4){

            steps[0].classList.add('hired');
            steps[1].classList.add('hired');
            steps[2].classList.add('hired');
            steps[3].classList.add('hired');

            lines.forEach(line => {

                line.classList.add('hired');

            });

        }

        // ==========================
        // RECHAZADO
        // ==========================
        else if (fase === 5){

            steps.forEach(step => {

                step.classList.add(
                    'disabled'
                );

            });

            steps[4].classList.remove(
                'disabled'
            );

            steps[4].classList.add(
                'rejected'
            );

        }

    }

});

document.addEventListener("DOMContentLoaded", function () {

    const filtro = document.getElementById("filtro-candidatos");
    const tabla = document.getElementById("tabla-candidatos");
    const filas = tabla.getElementsByTagName("tbody")[0].getElementsByTagName("tr");

    filtro.addEventListener("keyup", function () {

        let texto = filtro.value.toLowerCase();

        for (let i = 0; i < filas.length; i++) {

            // Columna Candidato (índice 1)
            let candidato = filas[i].cells[1].textContent.toLowerCase();

            // Columna Vacante (índice 2)
            let vacante = filas[i].cells[2].textContent.toLowerCase();

            if (
                candidato.includes(texto) ||
                vacante.includes(texto)
            ) {

                filas[i].style.display = "";

            } else {

                filas[i].style.display = "none";

            }
        }
    });

});