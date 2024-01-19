# author: Freek Baars
# date: 19-01-2024
# version: 1.1.0
# python 3.12.1

import eel
import serial.tools.list_ports
import serial
import threading
from threading import Lock
import time
import csv
import os
import tkinter as tk
from tkinter import filedialog



eel.init('programma/web')

# Globale variabelen
latest_weight = None
latest_angle_x = None
latest_angle_y = None
serial_instance = None
is_test_running = False

# Globale variabelen voor de CSV 
csv_bestandsnaam = "default_bestandsnaam"
csv_writer = None
csv_file = None
write_lock = Lock()
opslag_pad = os.getcwd()

# Globale variabelen voor sensorinstellingen
sensor_scalar = 1232 # 2kg 
sensor_unit_factor = 0.000001
sensor_eenheid = "G"

# Globale variabelen voor starttijd
start_tijd = None


def read_serial_data():
    global start_tijd, is_test_running, serial_instance, latest_weight, latest_angle_x, latest_angle_y
    while is_test_running and serial_instance and serial_instance.isOpen():
        if serial_instance.in_waiting > 0:
            data = serial_instance.readline().decode().strip()
            parts = data.split(',')
            if len(parts) == 3:
                weight, angle_x, angle_y = parts
                calibrated_weight = format_data(weight)

                latest_weight = calibrated_weight
                latest_angle_x = angle_x
                latest_angle_y = angle_y

                if start_tijd is not None:
                    verstreken_ms = int((time.time() * 1000) - start_tijd)
                    verstreken_sec = verstreken_ms // 1000
                    ms = verstreken_ms % 1000
                    verstreken_tijd_str = f"{verstreken_sec}:{ms:03d}"
                else:
                    verstreken_tijd_str = "0:000"

                with write_lock:
                    if csv_writer is not None:
                        csv_writer.writerow([verstreken_tijd_str, calibrated_weight, angle_x, angle_y])


def format_data(raw_data, precision=2):
    global sensor_scalar, sensor_unit_factor
    try:
        value = float(raw_data)
        calibrated_value = value * sensor_scalar
        unit_converted_value = calibrated_value * sensor_unit_factor
        return round(unit_converted_value, precision)
    except ValueError:
        return None


def create_unique_filename(base_path, base_name):
    counter = 1
    base_name_without_extension = os.path.splitext(base_name)[0]  # Verwijdert de extensie (indien aanwezig)
    unique_name = os.path.join(base_path, base_name_without_extension + '.csv')

    while os.path.exists(unique_name):
        unique_name = os.path.join(base_path, f"{base_name_without_extension}_{counter}.csv")
        counter += 1

    return unique_name


@eel.expose
def update_sensor_instellingen(scalar, eenheid):
    global sensor_scalar, sensor_unit_factor, sensor_eenheid
    print(f"update_sensor_instellingen aangeroepen met scalar: {scalar}, eenheid: {eenheid}")

    try:
        sensor_scalar = float(scalar)

        if eenheid == "gram":
            sensor_unit_factor = 0.000001
            sensor_eenheid = "G"
        elif eenheid == "newton":
            sensor_unit_factor = 0.00000981
            sensor_eenheid = "N"
        return True
    except Exception as e:
        print(f"Fout in update_sensor_instellingen: {e}")
        return False


@eel.expose
def set_map_pad(pad):
    global opslag_pad
    opslag_pad = pad   


def format_data(raw_data, scalar=sensor_scalar, offset=0.0, unit_factor=sensor_unit_factor, precision=2):
    """
    Kalibreert en formateert de ruwe data van de sensor.

    :param raw_data: De ruwe data van de sensor als een string.
    :param scalar: De kalibratiefactor voor de sensor.
    :param offset: De offsetwaarde voor nul kalibratie.
    :param unit_factor: De factor om de eenheid te converteren (bijv. van gram naar kilogram).
    :param precision: Het aantal decimalen voor afronding.
    :return: De gekalibreerde en geformatteerde waarde.
    """
    try:
        # Converteer de ruwe data naar een float
        value = float(raw_data)

        # Pas kalibratie toe
        calibrated_value = (value - offset) * scalar

        # Converteer naar de gewenste eenheid
        unit_converted_value = calibrated_value * unit_factor

        # Rond af tot de gewenste precisie
        return round(unit_converted_value, precision)
    except ValueError:
        return None


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
def get_latest_weight():
    global latest_weight
    return latest_weight

@eel.expose
def get_latest_angle_x():
    global latest_angle_x
    return latest_angle_x

@eel.expose
def get_latest_angle_y():
    global latest_angle_y
    return latest_angle_y


@eel.expose
def set_csv_bestandsnaam(bestandsnaam):
    global csv_bestandsnaam, opslag_pad
    csv_bestandsnaam = create_unique_filename(opslag_pad, bestandsnaam)
    print("Bestandsnaam voor CSV is ingesteld op:", csv_bestandsnaam)


@eel.expose
def start_test():
    global is_test_running, csv_bestandsnaam, csv_file, csv_writer, start_tijd, sensor_eenheid, opslag_pad
    if not is_test_running:
        # Als opslag_pad niet is ingesteld, gebruik de huidige werkmap
        if not opslag_pad:
            opslag_pad = os.getcwd()

        # Genereer een unieke bestandsnaam
        base_name = os.path.basename(csv_bestandsnaam) if csv_bestandsnaam else "default_bestandsnaam"
        unique_csv_bestandsnaam = create_unique_filename(opslag_pad, base_name)

        # Volledige pad voor het CSV-bestand
        volledige_pad = os.path.join(opslag_pad, unique_csv_bestandsnaam)
        csv_file = open(volledige_pad, mode='w', newline='', encoding='utf-8')
        csv_writer = csv.writer(csv_file)
        force_column_header = f"Force [{sensor_eenheid}]"
        csv_writer.writerow(['Time [S]', force_column_header, 'Angle X [deg]', 'Angle Y [deg]'])

        start_tijd = time.time() * 1000  # Tijd in milliseconden
        is_test_running = True
        threading.Thread(target=read_serial_data, daemon=True).start()
        print("Test gestart met bestandsnaam:", unique_csv_bestandsnaam)
    else:
        print("Test kan niet worden gestart. Is test running:", is_test_running, "Bestandsnaam:", csv_bestandsnaam)

@eel.expose
def stop_test():
    global is_test_running, csv_file, latest_force_reading
    if is_test_running:
        is_test_running = False
        latest_force_reading = None  # Reset de laatste krachtmeting
        if csv_file:
            csv_file.close()
            csv_file = None  # Reset csv_file na sluiting
        print("Test gestopt en CSV-bestand gesloten")
    else:
        print("Geen actieve test om te stoppen")



def close_callback(route, websockets):
    if not websockets:
        print("Websocket verbinding gesloten")
        exit()


eel.start('index.html', close_callback=close_callback)