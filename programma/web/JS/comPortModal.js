function initialiseerComPortModal() {
    // Toon de modal
    showComPortModal();

    // Voeg event listener toe aan de sluitknop
    document.querySelector('.close').addEventListener('click', function() {
        document.getElementById("comPortModal").style.display = "none";
    });
}

function showComPortModal() {
    var modal = document.getElementById("comPortModal");
    if (modal) {
        modal.style.display = "block";
    }
}

async function openSelectedPort(port) {
    let isOpened = await eel.open_serial_port(port)();
    if(isOpened) {
        alert("COM poort " + port + " succesvol geopend.");
        var modal = document.getElementById("comPortModal");
        modal.style.display = "none";
    } else {
        alert("Fout bij het openen van de poort");
    }
}