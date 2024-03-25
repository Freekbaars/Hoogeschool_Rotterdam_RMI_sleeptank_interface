# Hoogeschool_Rotterdam_RMI_sleeptank_interface

## Inleiding
voor mijn vrije kezedeel heb ik gekozen om een sleeptank interface te maken.
Deze keuze heb ik gemakt na dat een docent van mij zij dat er geen goede interface was voor de sleeptank. Dit klonk als een leuke uitdaging en heb ik deze opdracht aangenomen. 
Om de interface te maken heb ik gekozen om gebruik te maken van python en eel. Dit is een goede combinatie omdat ik al ervaring heb met python en eel is een goede manier om een web interface te maken met python. 

In het gebruik van HTML, CSS en JavaScript heb ik niet veel ervaring maar ik heb wel een basis kennis van deze talen.

## Installatie
De installatie is vrij simpel, je hoeft geen extra software te installeren. als je het exe bestand hebt gedownload is het klik en go.

Het is wel handig om een code editor te hebben zoals visual studio code of pycharm. als je aan pasingen wilt maken in de code.
hier voor moet je wel in eel de volgende aanpassing maken:
- eel (moet nog geüpdate worden voor 3.12 maar werkt wel als je de volgende stappen volgt)
    1. Find this import line:
        - import bottle.ext.websocket as wbs

    2. and replace it with the one below:
        - import bottle_websocket as wbs

## Gebruik
Om de interface te gebruiken moet je de volgende stappen volgen:
1. Plug metro m4 met de usb kabel in de computer, zorg dat alle sensoren zijn aangesloten!
2. Open programma
3. Selecteer COM. Port
4. Bevestig COM. Poort
5. Ga naar sleep test
6. Geef de test een naam (dit doe je door in het zij menu op de naam te klikken en een nieuwe naam in te voeren)
7. Bevestig deze naam
8. Klik op start test
9. Test loopt
10. Klik op stop test
11. Reset de grafiek
12. geef de test een nieuwe naam


## calibratie
Om de calibratie te doen moet je de volgende stappen volgen:
1. Open een code editor zoals visual studio code of pycharm.
2. Open de file calibratie.py
3. plug de metro m4 in de computer
4. run de code
5. volg de stappen in de terminal
6. sla de A en B warde op en voer deze in in de interface

### note
Wil je de calibratie permanet maken in het programma moet je de volgende stappen volgen:

1. Open het programma main.py
2. zoek de volgende code:
```python
# Globale variabelen voor sensorinstellingen
sensor_scalar = 0.00044721445660144023
sensor_offset = -0.3352244076764338
sensor_unit_factor = 9.81/1000
sensor_eenheid = "N"
```
3. vervang de waardes met de waardes die je hebt gekregen van de calibratie
    - sensor_scalar = A
    - sensor_offset = B

4. sla het bestand op
5. om er een nieuwe exe van te maken moet je de volgende stappen volgen:
    - run het volgende comando in de terminal:
    ```bash
    python -m eel programma\main.py programma\web --onefile 
    ```


## TODO
- [ ] .json file voor instelingen
- [ ] controleeren van alles 
 
## build comando
python to exe

```bash
python -m eel programma\main.py programma\web --onefile 
```

## benodigdheden
- metro m4
- 3d geprinte bakje
- HX711
- 1x load cell
