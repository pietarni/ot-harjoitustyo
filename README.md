*Ohjelmistotekniikka* **harjoitustyö**

## Viikko1

[Gitlog](https://github.com/pietarni/ot-harjoitustyo/blob/master/laskarit/viikko1/gitlog.txt)

[Komentorivi](https://github.com/pietarni/ot-harjoitustyo/blob/master/laskarit/viikko1/komentorivi.txt)


## Harjoitustö

[Vaatimusmäärittely](https://github.com/pietarni/ot-harjoitustyo/blob/master/harjoitustyo/dokumentaatio/vaatimusmaarittely.md)

[Tuntikirjanpito](https://github.com/pietarni/ot-harjoitustyo/blob/master/harjoitustyo/dokumentaatio/tuntikirjanpito.md)

[Changelog](https://github.com/pietarni/ot-harjoitustyo/blob/master/harjoitustyo/dokumentaatio/changelog.md)

Vaadittavien kirjastojen asentaminen:
ot-harjoitustyo/harjoitustyo/ poetry install

Ohjelman käynnistäminen:
ot-harjoitustyo/harjoitustyo/ poetry run invoke start


## Toiminta
Ohjelma pyytää käytättäjältä haluamansa alueen koordinaatit muodossa 'X,Y'.
Koordinaatit perustuvat lähtöhaineiston (kartta.hel.fi karkea maastomalli) indeksiruudukkoon, jossa ruutu 670491 on valittu origoksi. Täten jos haluaa löytää esim. Kruununhaan parhaat pulkkamäet, syötä koordinaatteina '6,3' ilman heittomerkkejä.
![image](https://user-images.githubusercontent.com/117778910/206023530-43be47f0-ee78-4930-abe1-4cace009fbc8.png)

Ohjelma lataa maastodataa, ja luo maastomallista "suuntakartan", eli 2D-listan jossa on analysoitu jokaisen pikselin kaltevuus. Tämä data on saatu kartta.hel.fi:stä
Sitten se lukee input-kansiosta rasteridataa teistä ja rakennuksista jne. Tämä data on saatu HSY:ltä. Se asettaa datat korkeusmallin mukaisesti.
### HUOM toistaiseksi tätä dataa on pakattuna ohjelman mukaan vain pohjois-arabianrannasta, eli tämä toimii toistaiseksi vain, jos käyttäjä syöttää koordinaatit 7,7. Pakkaan datan myöhemmin paremmin ladattavaksi erikseen, ettei ohjelman koko kasvaisi turhan suureksi

Sitten kartalle sijoitetaan käyttäjän valitsema määrä simuloituja pulkkailijoita kulkemaan mäkiä alas. Pulkkien reitit simuloidaan fyysikan kaavojen mukaisesti, ja piirretään Results/result.png kuvaan.

Esimerkki tästä lopputuloksesta: (mustavalkoinen on korkeuskarttaa, punainen merkitsee näitä pulkkamäen vaara-alueita)
![result](https://user-images.githubusercontent.com/117778910/206024386-c5b98d6c-47e2-40e7-bb05-d4d43b3c3f09.png)
