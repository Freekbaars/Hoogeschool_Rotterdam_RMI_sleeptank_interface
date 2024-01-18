let isTestActief = false;
let updateInterval;

//bazis functies
function resetGrafiek() {
    gewichtsChart.data.labels = []; // Labels resetten
    gewichtsChart.data.datasets.forEach((dataset) => {
        dataset.data = []; // Data resetten
    });
    gewichtsChart.update(); // Grafiek bijwerken om wijzigingen toe te passen
}

//zijmenu
function toggleZijmenu() {
    var zijmenu = document.getElementById("zijmenu");
    if (zijmenu.style.width === "250px") {
        zijmenu.style.width = "0";
    } else {
        zijmenu.style.width = "250px";
    }
}


//poorten
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
    if (isOpened) {
        console.log("Poort geopend: " + selectedPort);
    } else {
        console.log("Fout bij het openen van de poort");
    }
}


//sensoren
async function updateSensorInstellingen() {

    let scalar = document.getElementById('scalar-factor').value;
    let eenheid = document.getElementById('eenheid-select').value;

    // Valideer de invoer indien nodig

    // Stuur de gegevens naar de Python backend
    let resultaat = await eel.update_sensor_instellingen(naam, scalar, eenheid)();
    if (resultaat) {
        console.log("Sensorinstellingen bijgewerkt.");
    } else {
        console.log("Fout bij het bijwerken van sensorinstellingen.");
    }
}


//grafiek
var gewichtsChart;

function tekenGewichtsGrafiek() {
    var ctx = document.getElementById('Weerstand_Chart_1').getContext('2d');
    gewichtsChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],  // Tijdlabels
            datasets: [{
                label: 'Gewicht',
                data: [],  // Gewichtsdata
                // Voeg hier styling toe
            }]
        },
        options: {
            maintainAspectRatio: false,
        }
    });
}


async function updateGewichtsGrafiek() {
    if (!isTestActief) return;

    let gewichtsdata = await eel.get_latest_force_reading()();
    
    if (gewichtsdata !== null && gewichtsdata !== undefined) {
        let tijd = new Date().toLocaleTimeString();
        gewichtsChart.data.labels.push(tijd);
        gewichtsChart.data.datasets[0].data.push(gewichtsdata);
        gewichtsChart.update();
    }
}


//test-naam
let bestandsnaamBevestigd = false;

function bevestigBestandsnaam() {
    let bestandsnaam = document.getElementById('csv-bestandsnaam').value;
    if (bestandsnaam) {
        eel.set_csv_bestandsnaam(bestandsnaam)(function() {
            bestandsnaamBevestigd = true;
        });
    } else {
        alert('Voer een geldige bestandsnaam in.');
    }
}


//test-starten
async function startTest() {
    let bestandsnaam = document.getElementById('csv-bestandsnaam').value;
    if (bestandsnaam) {
        isTestActief = true;
        eel.start_test()(function() {
            updateInterval = setInterval(updateGewichtsGrafiek, 1000); // Start de interval om de grafiek bij te werken
        });
    } else {
        alert('Voer een geldige bestandsnaam in en bevestig.');
    }
}


//test-stoppen
function stopTest() {
    eel.stop_test()(); 
    isTestActief = false;
    clearInterval(updateInterval); // Stop de interval
    resetGrafiek(); // Reset de grafiek
}



window.onload = function() {
    loadSerialPorts();  // Laadt de seriële poorten
    tekenGewichtsGrafiek();  // Tekent de grafiek
    setInterval(updateGewichtsGrafiek, 1000); // Update de grafiek elke seconden
};