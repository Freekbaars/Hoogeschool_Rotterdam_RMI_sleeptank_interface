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
        }, 1000); // Zet de interval om de grafieken elke  seconde te updaten
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