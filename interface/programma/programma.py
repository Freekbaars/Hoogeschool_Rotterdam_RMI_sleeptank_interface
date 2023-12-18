# programma voor het uitlezen van de kracht sensor op de M4
# en het opslaan van de data in een csv bestand
# python 3.10.11
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
import os


# zoek de juiste poort ------------------------------------------------------

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






def main():
    portVar = find_serial_port()
    if portVar is None:
        print(f"COM{val} niet gevonden. Programma wordt afgesloten.")
        return

    serialInst = open_serial_port(portVar)

    
# run programma --------------------------------------------------------------
if __name__ == "__main__":
    start_time = datetime.now()
    main()

