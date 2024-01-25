// testnaam bevestigen 
function bevestigBestandsnaam() {
    let bestandsnaam = document.getElementById('csv-bestandsnaam').value;
    if (bestandsnaam) {
        eel.set_csv_bestandsnaam(bestandsnaam)(() => bestandsnaamBevestigd = true);
    } else {
        alert('Voer een geldige bestandsnaam in.');
    }
}

// opslaan map
function bevestigMapPad() {
    let mapPad = document.getElementById('map_pad').value;
    eel.set_map_pad(mapPad);
}
