# programma voor het uitlezen van de kracht sensor op de M4
# en het opslaan van de data in een csv bestand
# auteur: Freek Baars
# start datum: 06-11-2023

# importeer de benodigde modules ---------------------------------------------

import eel                                      # voor de web interface
import serial.tools.list_ports                  # voor het zoeken van de juiste poort
import matplotlib.pyplot as plt                 # voor het maken van de grafiek
from matplotlib.animation import FuncAnimation  # voor het updaten van de grafiek
import ujson                                    # voor het verwerken van de data
import pandas as pd                             # voor het opslaan van de data in een csv bestand
from datetime import datetime                   # voor het bijhouden van de tijd


# start web interface -------------------------------------------------------
eel.init("web")
eel.start("index.html")




# start test programma ------------------------------------------------------

# geef naam test document ---------------------------------------------------

naam_document = input("Geef de naam van het document: ")

# zoek de juiste poort ------------------------------------------------------
# todo maak een funtie voor het niet vinden van een COM poort
def find_serial_port():
    ports = list(serial.tools.list_ports.comports())
    portlist = []

    for p in ports:
        portlist.append(str(p.device))
        print(str(p.device))

    val = input("Selecteer de poort: COM")

    portVar = None
    for x in range(len(portlist)):
        if portlist[x].startswith("COM" + val):
            portVar = "COM" + val
            print(portlist[x])

    return portVar

# open de juiste poort ------------------------------------------------------
def open_serial_port(portVar):
    serialInst = serial.Serial()
    serialInst.baudrate = 9600
    serialInst.port = portVar

    try:
        serialInst.open()
    except Exception as e:
        print(f"Fout bij het openen van de poort {portVar}: {str(e)}")
        exit()

    return serialInst

# verwerk de data -----------------------------------------------------------
def process_sensor_data(packet, kracht_data, elapsed_time_data):
    stringN = packet.decode()
    string = stringN.rstrip()
    print(string)

    if "Verzonden gegevens" in string:
        try:
            data = ujson.loads(string.split("Verzonden gegevens: ")[1])
            kracht_data.append(data['kracht'])
            elapsed_time_data.append(datetime.now() - start_time)
        except ValueError:
            print(f"Kon de numerieke waarden niet uit de JSON-string halen: {string}")

# maak een functie voor het opslaan van de data -----------------------------
@eel.expose
def save_data():
    data_dict = {'Elapsed Time (s)': [td.total_seconds() for td in elapsed_time_data], 'Kracht': kracht_data}
    df = pd.DataFrame(data_dict)
    df.to_csv(naam_document, index=False)

# maak de grafiek -----------------------------------------------------------
def main():
    portVar = find_serial_port()
    if portVar is None:
        print(f"COM{val} niet gevonden. Programma wordt afgesloten.")
        return

    serialInst = open_serial_port(portVar)

    kracht_data = []   # A list to store force data
    elapsed_time_data = []      # A list to store elapsed time


    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
    fig.suptitle('Live Sensor Data')

    line_kracht, = ax1.plot([], [], lw=2, label='kracht')

    def update(frame):
        if serialInst.in_waiting:
            packet = serialInst.readline()
            process_sensor_data(packet, kracht_data, elapsed_time_data)

            line_kracht.set_data(range(len(kracht_data)), kracht_data)

            ax1.relim()
            ax1.autoscale_view()
            ax2.relim()
            ax2.autoscale_view()

    # Modify the FuncAnimation call here -------------------------------------
    ani = FuncAnimation(fig, update, frames=1000, repeat=False)

    plt.legend(handles=[line_kracht])
    plt.tight_layout()
    plt.show()

    # Save the data to a CSV file --------------------------------------------
    data_dict = {'Elapsed Time (s)': [td.total_seconds() for td in elapsed_time_data], 'Kracht': kracht_data}
    df = pd.DataFrame(data_dict)
    df.to_csv(naam_document, index=False)

    serialInst.close()

# run programma --------------------------------------------------------------
if __name__ == "__main__":
    start_time = datetime.now()
    main()
