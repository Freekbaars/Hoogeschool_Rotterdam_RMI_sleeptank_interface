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
            // Voeg hier grafiekopties toe
        }
    });
}

async function updateGewichtsGrafiek() {
    let gewichtsdata = await eel.get_latest_force_reading()();
    if (gewichtsdata) {
        let tijd = new Date().toLocaleTimeString(); // Huidige tijd voor de label
        gewichtsChart.data.labels.push(tijd);
        gewichtsChart.data.datasets[0].data.push(gewichtsdata);
        gewichtsChart.update();
    }
}


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

async function startTest() {
    if (bestandsnaamBevestigd) {
        await eel.start_test()();
    } else {
        alert('Bevestig eerst de bestandsnaam.');
    }
}


function stopTest() {
    eel.stop_test()();  // Roep de Python-functie aan om de test te stoppen
}



window.onload = function() {
    loadSerialPorts();  // Laadt de seriële poorten
    tekenGewichtsGrafiek();  // Tekent de grafiek
    setInterval(updateGewichtsGrafiek, 1000); // Update de grafiek elke seconden
};