# deze code loopt op de metro m4 (circuitpython)
# author: Freek Baars
# date: 19-01-2024
# version: 1.1.0

import board
from digitalio import DigitalInOut
from hx711.hx711_gpio import HX711_GPIO


# Definieer de GPIO pinnen voor de HX711
gpio_data = DigitalInOut(board.D5)
gpio_clk = DigitalInOut(board.D6)

# Maak het HX711 object aan
hx711 = HX711_GPIO(gpio_data, gpio_clk, tare=True)

# Hardcode de schaalfactor (vervang dit door jouw gekalibreerde waarde)
hx711.scalar = 1232  # Vervang dit door de werkelijke schaalfactor

# Functie om het gewicht te lezen
def get_weight():
    try:
        # Lees de gewogen waarde
        weight = hx711.read()
        return weight
    except OSError:
        # Handle leesfouten
        return None

# Hoofdlus om het gewicht continu te lezen
while True:
    weight = get_weight()
    if weight is not None:
        print(weight)
    else:
        print("Leesfout")
