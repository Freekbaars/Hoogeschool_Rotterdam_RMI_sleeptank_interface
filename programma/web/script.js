let isTestActief = false;
let updateInterval;
let startTijd;

// Basisfuncties
function resetGrafiek(chart) {
    chart.data.labels = []; // Labels resetten
    chart.data.datasets.forEach((dataset) => {
        dataset.data = []; // Data resetten
    });
    chart.update(); // Grafiek bijwerken om wijzigingen toe te passen
}

// Zijmenu
function toggleZijmenu() {
    var zijmenu = document.getElementById("zijmenu");
    zijmenu.style.width = zijmenu.style.width === "250px" ? "0" : "250px";
}

// Poorten laden
async function loadSerialPorts() {
    let ports = await eel.get_serial_ports()();
    let portsDropdown = document.getElementById('serial-ports-dropdown');
    ports.forEach(port => {
        let option = document.createElement('option');
        option.value = port;
        option.text = port;
        portsDropdown.appendChild(option);
    });
}

async function openSelectedPort() {
    let selectedPort = document.getElementById('serial-ports-dropdown').value;
    let isOpened = await eel.open_serial_port(selectedPort)();
    console.log(isOpened ? "Poort geopend: " + selectedPort : "Fout bij het openen van de poort");
}

// Sensorinstellingen bijwerken
async function updateSensorInstellingen() {
    let scalar = document.getElementById('scalar-factor').value;
    let eenheid = document.getElementById('eenheid-select').value;

    // Controleer of scalar een geldige waarde heeft
    if (!scalar) {
        alert("Voer een geldige scalar-waarde in.");
        return;
    }

    console.log(`Aanroepen update_sensor_instellingen met scalar: ${scalar}, eenheid: ${eenheid}`);
    let resultaat = await eel.update_sensor_instellingen(scalar, eenheid)();
    if (resultaat) {
        console.log("Sensorinstellingen bijgewerkt naar " + eenheid + ".");
        alert("Sensorinstellingen zijn bijgewerkt naar " + eenheid + ".");
    } else {
        console.log("Fout bij het bijwerken van sensorinstellingen.");
        alert("Fout bij het bijwerken van de sensorinstellingen.");
    }
}

// Grafiek voor gewicht
var gewichtsChart;

function tekenGewichtsGrafiek() {
    var ctx = document.getElementById('Weerstand_Chart_1').getContext('2d');
    gewichtsChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{ label: 'Gewicht', data: [] }]
        },
        options: { maintainAspectRatio: false }
    });
}

async function updateGewichtsGrafiek() {
    let gewichtsdata = await eel.get_latest_weight()();
    
    if (gewichtsdata !== null && gewichtsdata !== undefined) {
        // Zorg ervoor dat de deling door 1000 correct wordt uitgevoerd
        let verstrekenTijd = (Date.now() - startTijd) / 1000; 
        let verstrekenTijdAfgerond = verstrekenTijd.toFixed(2); // Rond af op twee decimalen

        gewichtsChart.data.labels.push(verstrekenTijdAfgerond); // Gebruik afgeronde verstreken tijd
        gewichtsChart.data.datasets[0].data.push(gewichtsdata);
        gewichtsChart.update();
    }
}

// Grafiek voor gyroscoop
var gyroChart;

function tekenGyroGrafiek() {
    var ctx = document.getElementById('Gyro_Chart').getContext('2d');
    gyroChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                { label: 'Hoek X', data: [], borderColor: 'red' },
                { label: 'Hoek Y', data: [], borderColor: 'blue' }
            ]
        },
        options: { maintainAspectRatio: false }
    });
}

async function updateGyroGrafiek() {
    if (!isTestActief) return;
    let hoekX = await eel.get_latest_angle_x()();
    let hoekY = await eel.get_latest_angle_y()();
    if (hoekX !== null && hoekX !== undefined && hoekY !== null && hoekY !== undefined) {
        let tijd = new Date().toLocaleTimeString();
        gyroChart.data.labels.push(tijd);
        gyroChart.data.datasets[0].data.push(hoekX);
        gyroChart.data.datasets[1].data.push(hoekY);
        gyroChart.update();
    }
}

// Testnaam bevestigen
function bevestigBestandsnaam() {
    let bestandsnaam = document.getElementById('csv-bestandsnaam').value;
    if (bestandsnaam) {
        eel.set_csv_bestandsnaam(bestandsnaam)(() => bestandsnaamBevestigd = true);
    } else {
        alert('Voer een geldige bestandsnaam in.');
    }
}

// Test starten
async function startTest() {
    let bestandsnaam = document.getElementById('csv-bestandsnaam').value;
    if (bestandsnaam) {
        startTijd = Date.now();
        isTestActief = true;
        await eel.start_test()();  // Zorg dat de test daadwerkelijk start voordat de interval begint
        updateInterval = setInterval(() => {
            updateGewichtsGrafiek();
            updateGyroGrafiek();
        }, 1000); // Zet de interval om de grafieken elke seconde te updaten
    } else {
        alert('Voer een geldige bestandsnaam in en bevestig.');
    }
}

// Test stoppen
function stopTest() {
    eel.stop_test()();
    isTestActief = false;
    clearInterval(updateInterval);
    resetGrafiek(gewichtsChart);
    resetGrafiek(gyroChart);
}

window.onload = function() {
    loadSerialPorts();
    tekenGewichtsGrafiek();
    tekenGyroGrafiek();
};
