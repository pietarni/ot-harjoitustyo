# Changelog

## Viikko 3

- Ohjelman pystyy invoke komennoilla startata ja testata
- Ohjelma lukee maastomallidatan, tekee siitä histogram of oriented gradients analyysin ja esittää sen maastomallin vieressä visuaalisesti. Tätä käytetään myöhemmin sopivien pulkkamäkirinteiden löytämiseen.

## Viikko 4
- Koska Histogram of Oriented gradientsista ei tiedä, mihin suuntaan mäki laskee, muutin sen omakoodatuksi direction mapiksi
- Ohjelma lukee dataa teistä ja rakennuksista ja muista alueista, johon pulkkamäki ei saa laskea
- Pulkkaajien matka simuloidaan fysiikan kaavoja käyttäen, reitit piirretään kartalle jossa näkyy maaston korkeus, vaara-alueet ja pulkkailijoiden reitit.

## Viikko 5
-Ohjelma lataa itsenäisesti Helsingin maastomalliaineistoa käyttäjän toivomalta alueelta
-Koodin siivousta, Pylintin käyttöönotto
-Käyttöliittymän kehitystä - käyttäjä voi syöttää ohjelmaan haluamansa alueen koordinaatit, ja simulaatiotiheyden
