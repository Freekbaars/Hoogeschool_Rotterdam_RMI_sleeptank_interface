# programma voor het uitlezen van de kracht sensor op de M4
# en het opslaan van de data in een csv bestand
# python 3.10.11
# auteur: Freek Baars
# start datum: 06-11-2023

# importeer de benodigde modules ---------------------------------------------
import eel
import serial
import serial.tools.list_ports
import time
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# int eel -------------------------------------------------------------

eel.init('web')

# eel variables -------------------------------------------------------
is_test_running = False

# Functie om de juiste seriële poort te vinden en te selecteren
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

# Functie om de geselecteerde seriële poort te openen
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


# DataFrame om de gegevens op te slaan
data = pd.DataFrame(columns=['Tijd', 'Gewicht'])

def lees_gewicht(serialInst):
    if serialInst.in_waiting > 0:
        line = serialInst.readline().decode('utf-8').rstrip()
        return line
    print(line)
    return None


def update_grafiek(frame):
    gewicht_str = lees_gewicht(ser)
    if gewicht_str is not None:
        gewicht = float(gewicht_str)  # Zet de string om naar een float
        print(gewicht)
        tijd = time.strftime("%Y-%m-%d %H:%M:%S")
        data.loc[len(data)] = [tijd, gewicht]
        plt.cla()
        plt.plot(data['Tijd'], data['Gewicht'], marker='o', color='b')
        plt.xticks(rotation=45, ha='right')
        plt.subplots_adjust(bottom=0.30)
        plt.title('Gewicht over Tijd')
        plt.ylabel('Gewicht (g)')
        plt.xlabel('Tijd')



def main():
    global ser, data
    selected_port = find_serial_port()
    ser = open_serial_port(selected_port)

    data = pd.DataFrame(columns=['Tijd', 'Gewicht'])

    fig = plt.figure()
    ani = FuncAnimation(fig, update_grafiek, interval=100)  # Update elke 1000 ms
    plt.show()

    # Opslaan naar CSV-bestand na afloop van het script
    data.to_csv('gewicht_data.csv', index=False)

if __name__ == "__main__":
    main()

