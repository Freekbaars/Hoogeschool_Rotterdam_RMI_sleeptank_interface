document.getElementById('startCalibratieKnop').addEventListener('click', function() {
    const aantalStappen = document.getElementById('aantal_stappen').value;
    const stapGrootte = document.getElementById('stap_grootte').value;
    eel.start_calibratie(aantalStappen, stapGrootte)();
});


// Functie om kalibratiefactor weer te geven
eel.expose(toon_kalibratie_factor);
function toon_kalibratie_factor(A, B) {
    document.getElementById('calibratie_resultaat').innerText = `Kalibratie factor: ${A}, Offset: ${B}`;
}


eel.expose(askSensorVastStaat);
function askSensorVastStaat(aantal_stappen, stap_grootte) {
    if (confirm("Staat de sensor vast?")) {
        // Simulatie van het registreren van een gewicht, vervang dit door je werkelijke logica
        for (let i = 0; i < aantal_stappen; i++) {
            eel.registreer_gewicht(i * stap_grootte)();
        }
        eel.bereken_kalibratie_factor();  // Roep de berekening aan na het voltooien van de datacollectie
    }
}

// Functie om de kalibratiefactor weer te geven
eel.expose(toon_kalibratie_factor);
function toon_kalibratie_factor(A) {
    document.getElementById('calibratie_resultaat').innerText = 'Kalibratie factor: ' + A;
}

function startCalibratie() {
    var aantalStappen = document.getElementById('aantal_stappen').value;
    var stapGrootte = document.getElementById('stap_grootte').value;
    console.log('Kalibratie gestart.');
    eel.start_calibratie(aantalStappen, stapGrootte)();
}


function tekenCalibratieGrafiek() {
    var ctx = document.getElementById('calibratie_grafiek').getContext('2d');
    var calibratieChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [], // X-as labels, bijvoorbeeld de gewichten
            datasets: [{
                label: 'Sensor Data',
                data: [], // Y-as gegevens, bijvoorbeeld de sensor readings
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}


// Functie om de grafiek bij te werken (moet nog worden geïmplementeerd)
eel.expose(updateCalibratieGrafiek);
function updateCalibratieGrafiek(gewicht) {
    // Voeg nieuwe data toe aan de grafiek
    calibratieChart.data.labels.push(gewicht);
    calibratieChart.data.datasets[0].data.push(sensor_reading);
    calibratieChart.update();
    console.log('Gewicht: ' + gewicht);  // Voor nu loggen we gewoon het gewicht
}