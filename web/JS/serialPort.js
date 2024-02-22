// Serial port dropdown vullen met beschikbare poorten
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