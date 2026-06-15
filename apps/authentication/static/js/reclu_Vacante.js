document.addEventListener('DOMContentLoaded', function () {

    const faseSelect = document.getElementById('fase_actual');

    actualizarTimeline();

    faseSelect.addEventListener('change', actualizarTimeline);

    function actualizarTimeline() {

        const fase = parseInt(faseSelect.value || 1);

        const step1 = document.getElementById('step1');
        const step2 = document.getElementById('step2');
        const step3 = document.getElementById('step3');

        const line1 = document.getElementById('line1');
        const line2 = document.getElementById('line2');

        [
            step1,
            step2,
            step3
        ].forEach(step => {

            step.classList.remove(
                'completed',
                'active'
            );
        });

        [
            line1,
            line2
        ].forEach(line => {

            line.classList.remove(
                'active'
            );
        });

        // =====================
        // FASE 1
        // =====================
        if (fase === 1) {

            step1.classList.add('active');
        }

        // =====================
        // FASE 2
        // =====================
        else if (fase === 2) {

            step1.classList.add('completed');

            line1.classList.add('active');

            step2.classList.add('active');
        }

        // =====================
        // FASE 3
        // =====================
        else if (fase >= 3) {

            step1.classList.add('completed');
            step2.classList.add('completed');

            line1.classList.add('active');
            line2.classList.add('active');

            step3.classList.add('active');
        }

    }

});