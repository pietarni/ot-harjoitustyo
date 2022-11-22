# Vaatimusmäärittely

## Sovelluksen tarkoitus

Sovelluksen avulla käyttäjä voi luoda ja katsella "pulkkamäki-karttoja". Ohjelmaan syötetään lähtödatana maanpintadataa (esim pistepilvi/korkeuskartta), ja ohjelma analysoi tästä parhaan mahdolliset pulkkamäet, ottamalla eri vaatimuksia huomioon.
Käyttäjä voi selailla tätä pulkkamäkikarttaa kautta, mahdollisesti graafisen käyttöliittymän kautta, jos tälläinen on realistista luoda python ohjelmalle, mutta vähintään .png-muotoista pulkkamäkikarttaa tutkimalla.

## Käyttöliittymä

Käyttöliittymässä käyttäjä antaa ohjelmalle joko hakemisto- tai url-osoitteen aineistoon, josta haluaa pulkkamäet löydettävän.
Ohjelma kysyy käyttäjältä vaatimuksia pulkkamäelle, ja ehdottaa valmiiksi valittuja vaatimuksia.
Ohjelma ilmoittaa kun pulkkamäkikartta on valmis, ja tätä voi selailla joko kuvana, tai sitten graafisessa käyttöliittymässä, jos sellainen onnistuu.

## Perusversion tarjoama toiminnallisuus

- Käyttäjä voi syöttää ohjelmaan maanpinta-aineiston.
  - Käyttäjä voi syöttää omia vaatimuksiansa pulkkamäelle (esim jyrkkyys, pituus)
    - Ohjelma sitten itsenäisesti etsii maanpinta-aineistosta vaatimuksiin sopivimmat mahdolliset pulkkamäet, merkitsee ne kartalle, esim. värittämällä ne .png-muotoisessa kuvassa
- Ohjelma voi myös itsenäisesti käydä läpiä suuria hajautettuja aineistoja, esim. kartta.hel.fi:n aineistot, ja luoda näistä suurempia pulkkamäkikarttoja.
- Pulkkamäkien tiedot ovat tallennettu tietokantaan, esim. niiden sijainnit ja arvioitu soveltuvuus pulkkamäkeilyyn.

## Jatkokehitysideoita

Perusversion jälkeen järjestelmää täydennetään ajan salliessa esim. seuraavilla toiminnallisuuksilla:

- Graafinen käyttöliittymä, jossa on helppo selailla eri pulkkamäkiä, ja lukea niiden tietoja suoraan kartalta.
