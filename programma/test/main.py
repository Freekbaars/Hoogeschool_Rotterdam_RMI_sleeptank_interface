import eel
import serial.tools.list_ports
import serial
import threading
from threading import Lock
import pandas as pd
import time
import csv

eel.init('web')  # Vervang met het pad naar je web map

# Globale variabele voor het bijhouden van de laatste krachtmeting
latest_force_reading = None
serial_instance = None
is_test_running = False
data_frame = None
csv_bestandsnaam = None
csv_writer = None
csv_file = None  # Dit zorgt ervoor dat csv_file globaal beschikbaar is
write_lock = Lock()



def read_serial_data():
    global is_test_running, serial_instance, csv_writer,  latest_force_reading
    while is_test_running and serial_instance and serial_instance.isOpen():
        if serial_instance.in_waiting > 0:
            data = serial_instance.readline().decode().strip()
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")

            latest_force_reading = data

            with write_lock:
                if csv_writer is not None:
                    csv_writer.writerow([current_time, data])
                else:
                    print("csv_writer is None, kan niet naar CSV-bestand schrijven")


@eel.expose
def get_serial_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]
print(get_serial_ports())


@eel.expose
def open_serial_port(portVar):
    global serial_instance, is_test_running
    try:
        serial_instance = serial.Serial(portVar, baudrate=9600, timeout=1)
        print("Seriële poort geopend:", portVar)
        if not is_test_running:
            threading.Thread(target=read_serial_data, daemon=True).start()
            print("Seriële lees thread gestart")
        return True
    except Exception as e:
        print(f"Fout bij het openen van de poort {portVar}: {str(e)}")
        return False

@eel.expose
def get_latest_force_reading():
    global latest_force_reading
    return latest_force_reading


@eel.expose
def set_csv_bestandsnaam(bestandsnaam):
    global csv_bestandsnaam
    csv_bestandsnaam = bestandsnaam
    print("Bestandsnaam voor CSV is ingesteld op:", csv_bestandsnaam)


@eel.expose
def start_test():
    global is_test_running, csv_bestandsnaam, csv_file, csv_writer
    if not is_test_running and csv_bestandsnaam:
        is_test_running = True

        csv_file = open(csv_bestandsnaam + '.csv', mode='w', newline='', encoding='utf-8')
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Tijd', 'Data'])

        threading.Thread(target=read_serial_data, daemon=True).start()
        print("Test gestart met bestandsnaam:", csv_bestandsnaam)
    else:
        print("Test kan niet worden gestart. Is test running:", is_test_running, "Bestandsnaam:", csv_bestandsnaam)



@eel.expose
def stop_test():
    global is_test_running, csv_file
    if is_test_running:
        is_test_running = False
        if csv_file:
            csv_file.close()
            csv_file = None  # Reset csv_file na sluiting
        print("Test gestopt en CSV-bestand gesloten")
    else:
        print("Geen actieve test om te stoppen")


eel.start('index.html')
