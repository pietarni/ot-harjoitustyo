
## Ohjelman rakenne

DataHandler- luokka lataa ja käsittelee korkeusdatan Helsingin avoimesta rajapinnasta. Se luo DirectionMap-luokan ilmentymän, joka käsittelee korkeusdatasta "suuntakartan"
SimulationUnit- luokka merkitsee yksittäistä simuloitua pulkkailijaa. Luokka on riippuvainen DirectionMap-luokasta, sillä se lukee sen dataa määrittääkseen oman reittinsä maastossa.
ResultDataCreator- luokka luo GeoJSON tiedoston pulkkailijoiden reittien perusteella

![luokkakaavio](https://github.com/pietarni/ot-harjoitustyo/blob/master/harjoitustyo/dokumentaatio/kuvat/luokkakaavio.png)

## Ohjelman toiminta

Ohjelman koko toimintaa kuvaa sekvenssikaavio:
![sekvenssikaavio](https://github.com/pietarni/ot-harjoitustyo/blob/master/harjoitustyo/dokumentaatio/kuvat/sekvenssikaavio.png)

Käyttäjä antaa ohjelmalle tiedon haluamansa alueen koordinaateista, sekä "simulaatiotiheydestä".
Ohjelma palauttaa käyttäjälle kuvan result.png ja [geojson](https://geojson.org/) tiedoston result.json. GeoJSON tiedostoa voi tutkia esim QGis-ohjelmassa.
