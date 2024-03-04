// Sensorinstellingen bijwerken 
async function updateSensorInstellingen() {
    let scalar = document.getElementById('scalar-factor').value;
    let offset = document.getElementById('scalar-offset').value; // Zorg dat dit ID correct is
    let eenheid = document.getElementById('eenheid-select').value;

    // Controleer of scalar en offset geldige waarden hebben
    if (!scalar || !offset) {
        alert("Voer geldige waarden in voor zowel scalar als offset.");
        return;
    }

    console.log(`Aanroepen update_sensor_instellingen met scalar: ${scalar}, offset: ${offset}, eenheid: ${eenheid}`);
    let resultaat = await eel.update_sensor_instellingen(scalar, offset, eenheid)();
    if (resultaat) {
        console.log("Sensorinstellingen bijgewerkt.");
        alert("Sensorinstellingen succesvol bijgewerkt.");
    } else {
        console.log("Fout bij het bijwerken van sensorinstellingen.");
        alert("Fout bij het bijwerken van de sensorinstellingen.");
    }
}