import serial
import time

# Pas deze aan naar de juiste COM-poort
com_port = 'COM14'  # Voorbeeld voor Windows

with serial.Serial(com_port, baudrate=9600, timeout=1) as serial_instance:
    while True:
        if serial_instance.in_waiting > 0:
            data = serial_instance.readline().decode().strip()
            print("Ontvangen data:", data)
            
        time.sleep(0.1)  # Kleine pauze om CPU te ontlasten

