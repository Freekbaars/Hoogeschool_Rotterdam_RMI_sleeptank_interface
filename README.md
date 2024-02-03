# Hoogeschool_Rotterdam_RMI_sleeptank_interface

## Inleiding
voor mijn vrije kezedeel heb ik gekozen om een sleeptank interface te maken.

## Installatie
de installatie is vrij simpel, je moet de volgende dingen installeren:
- python 3.12
- pyserial
- eel (moet nog geubdate worden voor 3.12 maar werkt wel als je de volgende stappen volgt)
    1. Find this import line:
        - import bottle.ext.websocket as wbs

    2. and replace it with the one below:
        - import bottle_websocket as wbs

## Gebruik
Om de interface te gebruiken moet je de volgende stappen volgen:
1. Plug metro m4 in je pc
2. Open programma
3. Selecteer COM. Port
4. Bevestig COM. Poort
5. Geef de test een naam
6. Bevestig deze naam
7. Klik op start test
8. Test loopt
9. Klik op stop test
10. geef de test een nieuwe naam

