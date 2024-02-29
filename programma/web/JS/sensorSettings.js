// Sensorinstellingen bijwerken 
async function updateSensorInstellingen() {
    let scalar = document.getElementById('scalar-factor').value;
    let offset = document.getElementById('scaler-offcet').value;
    let eenheid = document.getElementById('eenheid-select').value;

    // Controleer of scalar een geldige waarde heeft
    if (!scalar) {
        alert("Voer een geldige scalar-waarde in.");
        return;
    }

    console.log(`Aanroepen update_sensor_instellingen met scalar: ${scalar}, eenheid: ${eenheid}`);
    let resultaat = await eel.update_sensor_instellingen(scalar, offset, eenheid)();
    if (resultaat) {
        console.log("Sensorinstellingen bijgewerkt naar " + eenheid + ".");
        alert("Sensorinstellingen zijn bijgewerkt naar " + eenheid + ".");
    } else {
        console.log("Fout bij het bijwerken van sensorinstellingen.");
        alert("Fout bij het bijwerken van de sensorinstellingen.");
    }
}