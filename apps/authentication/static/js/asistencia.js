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
