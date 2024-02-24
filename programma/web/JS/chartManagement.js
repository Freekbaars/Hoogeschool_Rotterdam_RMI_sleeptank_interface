// Grafiek voor gewicht
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

// Gewichtsgrafiek updaten
async function updateGewichtsGrafiek() {
    let gewichtsdata = await eel.get_latest_weight()();
    
    if (gewichtsdata !== null && gewichtsdata !== undefined) {
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

// Gyrografiek updaten
async function updateGyroGrafiek() {
    if (!isTestActief) return;
    let hoekX = await eel.get_latest_angle_x()();
    let hoekY = await eel.get_latest_angle_y()();
    if (hoekX !== null && hoekX !== undefined && hoekY !== null && hoekY !== undefined) {
        let verstrekenTijd = (Date.now() - startTijd) / 1000; 
        let verstrekenTijdAfgerond = verstrekenTijd.toFixed(2);

        gyroChart.data.labels.push(verstrekenTijdAfgerond);
        gyroChart.data.datasets[0].data.push(hoekX);
        gyroChart.data.datasets[1].data.push(hoekY);
        gyroChart.update();
    }
}


// Grafiek voor kalibratie
function tekenKalibratieGrafiek() {
    var ctx = document.getElementById('Kalibratie_Chart').getContext('2d');
    gewichtsChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{ label: 'Gewicht', data: [] }]
        },
        options: { maintainAspectRatio: false }
    });
}

// kalibratie grafiek updaten
async function updateKalibratieGrafiek() {
    let gewichtsdata = await eel.get_latest_weight()();
    
    if (gewichtsdata !== null && gewichtsdata !== undefined) {
        let verstrekenTijd = (Date.now() - startTijd) / 1000; 
        let verstrekenTijdAfgerond = verstrekenTijd.toFixed(2); // Rond af op twee decimalen

        gewichtsChart.data.labels.push(verstrekenTijdAfgerond); // Gebruik afgeronde verstreken tijd
        gewichtsChart.data.datasets[0].data.push(gewichtsdata);
        gewichtsChart.update();
    }
}

// Grafiek resetten (labels en data verwijderen)
function resetGrafiek(chart) {
    chart.data.labels = []; // Labels resetten
    chart.data.datasets.forEach((dataset) => {
        dataset.data = []; // Data resetten
    });
    chart.update(); // Grafiek bijwerken om wijzigingen toe te passen
}


// Initialisatie functie voor grafieken
function initialiseerGrafieken() {
    if (document.getElementById('Weerstand_Chart_1')) {
        tekenGewichtsGrafiek();
    }
    if (document.getElementById('Gyro_Chart')) {
        tekenGyroGrafiek();
    }
    if (document.getElementById('Kalibratie_Chart')) {
        tekenKalibratieGrafiek();
    }
}