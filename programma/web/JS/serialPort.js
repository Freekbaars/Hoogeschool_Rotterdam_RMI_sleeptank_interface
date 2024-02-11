// Serial port dropdown vullen met beschikbare poorten
async function loadSerialPorts() {
    let ports = await eel.get_serial_ports()(); // Ophalen van de poorten
    let portsDropdown = document.getElementById('serial-ports-dropdown');
    portsDropdown.innerHTML = ''; // Maak de dropdown leeg voor het geval dat
    ports.forEach(port => {
        let option = document.createElement('option');
        option.value = port;
        option.text = port;
        portsDropdown.appendChild(option);
    });
    showComPortModal(); // Toon de modal nadat de poorten geladen zijn
}

function showComPortModal() {
    var modal = document.getElementById('comPortModal');
    modal.style.display = 'block'; // Toon de modal
}

// Serial port openen
async function openSelectedPort() {
    let selectedPort = document.getElementById('serial-ports-dropdown').value;
    let isOpened = await eel.open_serial_port(selectedPort)();
    console.log(isOpened ? "Poort geopend: " + selectedPort : "Fout bij het openen van de poort");
}

function selectAndOpenPort() {
    var selectedPort = document.getElementById('serial-ports-dropdown').value;
    openSelectedPort(selectedPort);
}

function showComPortModal() {
    var modal = document.getElementById("comPortModal");
    modal.style.display = "block";
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

document.querySelector('.close').addEventListener('click', function() {
    document.getElementById("comPortModal").style.display = "none";
});
