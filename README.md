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

Ohjelmassa ei toistaiseksi ole käyttöliittymää, se käyttää kovakoodattua tietoa ja dataa, jota se saa mm. input-kansiosta.

## Toiminta
Ohjelma pyytää käytättäjältä haluamansa alueen koordinaatit muodossa 'X,Y'.
Koordinaatit perustuvat lähtöhaineiston (kartta.hel.fi karkea maastomalli) indeksiruudukkoon, jossa ruutu 670491 on valittu origoksi. Täten jos haluaa löytää esim. Kruununhaan parhaat pulkkamäet, syötä koordinaatteina '6,3' ilman heittomerkkejä.
![image](https://user-images.githubusercontent.com/117778910/206023530-43be47f0-ee78-4930-abe1-4cace009fbc8.png)

Ohjelma lataa maastodataa, ja luo maastomallista "suuntakartan", eli 2D-listan jossa on analysoitu jokaisen pikselin kaltevuus. Tämä data on saatu kartta.hel.fi:stä
Sitten se lukee input-kansiosta rasteridataa teistä ja rakennuksista jne. Tämä data on saatu HSY:ltä. Se asettaa datat korkeusmallin mukaisesti.

Sitten kartalle sijoitetaan käyttäjän valitsema määrä simuloituja pulkkailijoita kulkemaan mäkiä alas. Pulkkien reitit simuloidaan fyysikan kaavojen mukaisesti, ja piirretään Results/result.png kuvaan.
